#! /usr/bin/env python

__version__ = '0.0.1'

import sys
import os
from share import *

nMAX = 10
eMAX = 13

# #########################################

def contain( lst, elem ) :
	return [ i for i, e in enumerate( lst ) if e[:2] == elem[:2] ]

# #########################################

if __name__ == '__main__' :
	print '\nVERSION: %s\n' % __version__
	os.chdir( os.path.join( os.getcwd(), os.path.dirname( __file__ ) ) )
	
	try :
		RANDOM = sys.argv[1]
	except :
		RANDOM = ''
	
	if RANDOM == 'bg' :
		deg_dim_file = 'bg_deg-dim_file'
		scatter_file = 'bg_scatter_file'
	else :
		deg_dim_file = 'deg-dim_file'
		scatter_file = 'scatter_file'
	
	scatter = []
	for n in range( 2, nMAX+1 ) :
		for e in range( n, eMAX+1 ) :
			fileDict = gen_file_dict( n, e )
			if os.path.isfile( fileDict[deg_dim_file] ) :
				for deg_dim in eval( open( fileDict[deg_dim_file], 'r' ).read() ) :
					num = contain( scatter, deg_dim )
					if not num :
						scatter.append( deg_dim )
					else :
						scatter[ num[0] ][2] += deg_dim[2]
	
	open( fileDict[scatter_file], 'w' ).write( str( scatter ).replace( '[', '{' ).replace( ']', '}' ) )
	