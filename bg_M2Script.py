#! /usr/bin/env python

__version__ = '0.0.2'

import sys
import os
import time
import hashlib
import MySQLdb
from share import *

# ################################

def md5rand() :
	m = hashlib.md5()
	m.update( time.ctime() )
	m.update( time.ctime() )
	return m.hexdigest()[:4]

# ################################

os.chdir( os.path.join( os.getcwd(), os.path.dirname( __file__ ) ) )
globNode, globEdge = wait_for_ne( sys.argv[1:] )
fileDict = gen_file_dict( globNode, globEdge )
if not check_folder( False, fileDict['bg_m2in_folder'] ) :
	print "\n!!! Can not find background M2-file folder. Quit..."
	my_quit( 2 )
check_folder( True, fileDict['bg_m2out_folder'], fileDict['temp'] )

try :
	maxNumber = eval( open( fileDict['count_file'], 'r' ).read() )
except :
	print 'Error reading <count.txt> file. Quit...'
	my_quit( 1 )

try :
	begin = max( 1, int( sys.argv[3] ) )
except :
	begin = 1

try :
	end = min( maxNumber, int( sys.argv[4] ) )
	try :
		if begin == end :
			APPEND = int( sys.argv[5] )
		else :
			APPEND = 1
	except :
		APPEND = 1
except :
	APPEND = 1
	end = maxNumber

if begin > end :
	print '\nBeginning file number should not be greater than ending file number. Quit...\n'
	my_quit( 1 )


def gen_m2out( path, k ) :
	global globNode, globEdge, APPEND
	
	state, count = 0, 0
	TEMP = os.path.join( fileDict['temp'], 'bg_%d_%d_%d_%s.m2o' % ( globNode, globEdge, k, md5rand() ) )
	
	f = open( path, 'r' )
	EXEC = 'M2 << EOF >> /dev/null\n'
	for line in f :
		if line == '\n' :
			if '_r' in path :
				file = fileDict['bg_m2out_r_file'] % k
				RANDOM = '_r'
			else :
				file = fileDict['bg_m2out_file'] % k
				RANDOM = ''
			
			count += 1
			EXEC += '"%s" << toString({dim(V),degree(V),hilbertSeries(V)})|"\\n" << close;\nEOF\n' % TEMP
			
			if count >= APPEND :
				state = os.system( EXEC )
			
			if state :
				print '\nstate = %d' % state
				print '\nTerminated @ FILE = %06d_bg(_r).m2 & NUMBER = %d.\n' % ( k, count )
				open( file, 'a' ).write( '{}\n' )
			elif count == 1 and APPEND == 1 :
				open( file, 'w' ).write( open( TEMP, 'r' ).read() )
			elif count >= APPEND :
				open( file, 'a' ).write( open( TEMP, 'r' ).read() )
			
			print '........ N_E = %d_%d ........ %d -> %d ........ Done %d in %06d_bg%s.m2' % ( globNode, globEdge, begin, end, count, k, RANDOM )
			EXEC = 'M2 << EOF >> /dev/null\n'
		else :
			EXEC += line
	f.close()
	
	try :
		os.remove( TEMP )
	except :
		print '\nNo computation needs to be done.'


start = time.time()
curr = begin
while curr <= end :
	for name in [ '%06d_bg.m2' % curr, '%06d_bg_r.m2' % curr ] :
		path = os.path.join( fileDict['bg_m2in_folder'], name )
		if os.path.exists( path ) and os.path.isfile( path ) :
			gen_m2out( path, curr )
			print '================================ DONE ================================\n'
			break
	curr += 1
print_time( time.time() - start )


try :
	conn = MySQLdb.connect( host='210.45.114.84', user='day', passwd='299792458', db='projects' )
	cursor = conn.cursor()
	cursor.execute( "INSERT INTO done(n,e,begin,end) VALUES(%d,%d,%d,%d)" % ( globNode, globEdge, begin, end ) )
	conn.commit()
	print "\n Successfully write into the database.\n"
except :
	print "\n Fail to write into the database.\n"
