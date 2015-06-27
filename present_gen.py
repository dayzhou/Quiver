#! /usr/bin/env python

r"""
Generate data files for M2 to calculate
"""

__version__ = '0.0.6'

import sys
import os
import time
from share import *

globBaseNumber = 3

# #####################################

def to_math_form( quiver ) :
	quiver = str( map( lambda cycle: map( lambda n: n+1, cycle ), eval( quiver ) ) )
	return '%s\n' % quiver.replace( '[', '{' ).replace( ']', '}' )


def get_total_spot_number( k ) :
	num = 0
	for line in open( fileDict['gio_file'] % k, 'r' ) :
		if line.count( 'Superscript' ) > 2 :
			num += 1
	return ( globBaseNumber ** num - 1 ) / 2


def add_to_this_dict( dict, key ) :
	if dict.has_key( key ) :
		dict[key] += 1
	else :
		dict[key] = 1
	dict['sum'] += 1


def add_to_dict( dict, thisDict, total ) :
	dict['sum'] += total
	sample = float( thisDict['sum'] )
	del thisDict['sum']
	for key in thisDict.keys() :
		if dict.has_key( key ) :
			dict[key] += thisDict[key] * total / sample
		else :
			dict[key] = thisDict[key] * total / sample
	

def write_to_dict( dict, filename ) :
	total = float( dict['sum'] )
	del dict['sum']
	keys = dict.keys()
	keys.sort()
	res = ''
	for key in keys :
		res += '{%d, %.8f}, ' % ( key, dict[key] * 100 / total )
	f = open( filename, 'w' )
	f.write( '{%s}' % res[:-2] )
	f.close()


def gen_present_files() :
	global globNode, globEdge
	dimDict, degDict = {'sum':0}, {'sum':0}
	graphNumber = eval( open( fileDict['count_file'], 'r' ).read() )
	
	for i, quiver in enumerate( open( fileDict['quiver_file'], 'r' ) ) :
		quiver = to_math_form( quiver )
		print '\n----------------- QUIVER: {:,} -----------------'.format( i+1 )
		
		try :
			fspot = open( fileDict['spot_file'] % (i+1), 'r' )
			outFile = fileDict['m2out_file'] % (i+1)
			presentFile = fileDict['present_file'] % (i+1)
		except :
			try :
				fspot = open( fileDict['spot_r_file'] % (i+1), 'r' )
				outFile = fileDict['m2out_r_file'] % (i+1)
				presentFile = fileDict['present_r_file'] % (i+1)
			except :
				print 'No SuperPotential file is found.'
				continue
		
		try :
			fout = open( outFile, 'r' )
		except :
			print 'No M2 Output file is found.'
			continue
		
		totalSpot = get_total_spot_number( i+1 )
		
		fpr = open( presentFile, 'w' )
		fpr.write( quiver )
		thisDimDict, thisDegDict = {'sum':0}, {'sum':0}
		for superpotential in fspot :
			try :
				dimension, degree = map( eval, fout.readline().strip( '{' ).split( ',' )[:2] )
				add_to_this_dict( thisDimDict, dimension )
				add_to_this_dict( thisDegDict, degree ) 
			except :
				continue
			else :
				fpr.write( '{%s, %d, %d}\n' % ( superpotential.strip( '\n' ), dimension, degree ) )
		add_to_dict( dimDict, thisDimDict, totalSpot )
		add_to_dict( degDict, thisDegDict, totalSpot )
		
		print '---------- N_E = %d_%d ---------- DONE' % ( globNode, globEdge )
		fpr.close()
	
	write_to_dict( dimDict, fileDict['dim_file'] )
	write_to_dict( degDict, fileDict['deg_file'] )

# #####################################

if __name__ == '__main__' :
	os.chdir( os.path.join( os.getcwd(), os.path.dirname( __file__ ) ) )
	print '\nVERSION: %s\n' % __version__
	
	globNode, globEdge = wait_for_ne( sys.argv[1:] )
	fileDict = gen_file_dict( globNode, globEdge )
	
	if not check_file( fileDict['count_file'], fileDict['quiver_file'] ) or not check_folder( False, fileDict['spot_folder'], fileDict['m2out_folder'], fileDict['gio_folder'] ) :
		print 'The quiver file or superpotential files or M2Out files do not exist. Quit...'
		my_quit( 2 )
	check_folder( True, fileDict['present_folder'] )
	
	start = time.time()
	gen_present_files()
	print_time( time.time() - start )
	