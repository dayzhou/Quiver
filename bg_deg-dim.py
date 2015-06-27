#! /usr/bin/env python

__version__ = '0.0.2'

import sys
import os
from share import *

globBaseNumber = 11

# #########################################

def get_total_spot_number( k ) :
	num = 0
	for line in open( fileDict['gio_file'] % k, 'r' ) :
		if line.count( 'Superscript' ) > 2 :
			num += 1
	return ( globBaseNumber ** num - 1 ) / 2


def contain( lst, elem ) :
	return [ i for i, e in enumerate( lst ) if e[:2] == elem[:2] ]


def read_deg_dim( fpr, totalSpot ) :
	fpr.readline()
	deg_dim_list = []
	total = 0
	
	for line in fpr :
		total += 1
		dim_deg = map( int, line.lstrip( '{' ).rstrip( '}\n' ).split( ',' )[-2:] )
		dim_deg.reverse()
		num = contain( deg_dim_list, dim_deg )
		if not num :
			deg_dim_list.append( dim_deg + [1] )
		else :
			deg_dim_list[ num[0] ][2] += 1
	
	if total < totalSpot :
		for deg_dim in deg_dim_list :
			deg_dim[2] = float( deg_dim[2] ) * totalSpot / total
	
	return deg_dim_list


def add_to_deg_dim_list( newList, deg_dim_list ) :
	for deg_dim in newList :
		num = contain( deg_dim_list, deg_dim )
		if not num :
			deg_dim_list.append( deg_dim )
		else :
			deg_dim_list[ num[0] ][2] += deg_dim[2]

# #########################################

if __name__ == '__main__' :
	print '\nVERSION: %s' % __version__
	os.chdir( os.path.join( os.getcwd(), os.path.dirname( __file__ ) ) )
	globNode, globEdge = wait_for_ne( sys.argv[1:] )
	fileDict = gen_file_dict( globNode, globEdge )
	if not check_file( fileDict['count_file'] ) or not check_folder( False, fileDict['bg_present_folder'], fileDict['gio_folder'] ) :
		print "\n!!! Can not find count_file or bg_present_folder or gio_folder. Quit..."
		my_quit( 1 )
	
	deg_dim_list = []
	for i in range( eval( open( fileDict['count_file'], 'r' ).read() ) ) :
		print '\n----------------- QUIVER: {:,} -----------------'.format( i+1 )
		
		try :
			fpr = open( fileDict['bg_present_file'] % (i+1), 'r' )
		except :
			try :
				fpr = open( fileDict['bg_present_r_file'] % (i+1), 'r' )
			except :
				print 'No present_file is found.'
				continue
		
		add_to_deg_dim_list( read_deg_dim( fpr, get_total_spot_number( i+1 ) ), deg_dim_list )
	
	content = str( [ [ deg, dim, int( round( count ) ) ] for deg, dim, count in deg_dim_list ] )
	open( fileDict['bg_deg-dim_file'], 'w' ).write( content )
	open( fileDict['bg_deg-dim_math_file'], 'w' ).write( content.replace( '[', '{' ).replace( ']', '}' ) )
