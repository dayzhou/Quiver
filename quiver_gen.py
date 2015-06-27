#! /usr/bin/env python

r"""
Generate quiver files for given numbers of nodes and edges.
"""

__version__ = '0.3.3'

import sys
import os
import time
import igraph as ig
from share import *

# #########################################

globNode = 0
globEdge = 0

globCurrSizeList = []
globSizeLists = []

globDisconnectedGraphList = []
globCurrGraphList = []
globGraphList = []

globMaxSize = 0
globCounter = 0
globCycleList = []

globOutputFile = None

# #########################################

def first_non_zero( theList ) :
	for i, elem in enumerate( theList ) :
		if elem : return i
	return -1


def is_primary( theList ) :
	zero, one = theList.count(0), theList.count(1)
	if zero == len( theList ) - 1 and one == 1 :
		return True
	return False


def output( STR ) :
	print STR
	globOutputFile.write( STR+'\n' )


def reduce_size_list( theList ) :
	tempList = theList[:]
	tempList[ first_non_zero( tempList ) ] -= 1
	return tempList


def get_e_from_( theList ) :
	return inner_prod( range( 1, len( theList )+1 ), theList )


def make_graph_from_( n, loops ) :
	gr = ig.Graph( n=n, directed=True )
	for loop in loops :
		gr.add_edges( list_to_edges( loop, closed=False ) )
	return gr

# #########################################

def connectedness( sizeList ) :
	return inner_prod( sizeList, range( len( sizeList ) ) ) + 1


def recur_size_list( cEdge, tempList, cycle=[] ) :
	if len( tempList ) == 1 :
		if cEdge != globEdge :
			globSizeLists.append( [cEdge]+cycle )
		return
	
	tempLast, tempRest = tempList[-1], tempList[:-1]
	for j in tempLast :
		if j <= cEdge :
			recur_size_list( cEdge-j, tempRest, [j]+cycle )


def calc_size_list() :
	global globSizeLists
	
	tempList = []
	for i in range( 1, globNode+1 ) :
		tempList.append( range( 0, globEdge+1, i ) )
	
	recur_size_list( globEdge, tempList )
	
	for i in range( len( globSizeLists ) ) :
		for j in range( globNode ) :
			globSizeLists[i][j] /= j + 1
	
	globSizeLists = filter(
		lambda s: connectedness(s) >= globNode or s[0] == 0,
		globSizeLists
	)
	
	output( '\n___ Number of cycle size combinations: %d' % len( globSizeLists ) )
	output( '___ Connected cycle size combinations: %d\n' % len( [ s for s in globSizeLists if connectedness(s) >= globNode ] ) )
	return len( globSizeLists )

# #########################################

def recur_cycle( trail, gr ) :
	if trail[-1].target == trail[0].source :
		globCycleList.append( [ e.source for e in trail ] + [ trail[0].source ] )
		gr.delete_edges( [ e.index for e in trail ] )
		return True
	elif trail[-1].target in [ e.source for e in trail ] :
		return False
	else :
		for e in gr.es.select( _source=trail[-1].target ) :
			if recur_cycle( trail+[e], gr ) :
				return True


def find_cycle_list( gr ) :
	gr = gr.copy()
	while len( gr.es ) :
		recur_cycle( [ gr.es[0] ], gr )

# #########################################

def write_to_quiver_file() :
	global globCycleList
	fh = open( fileDict['quiver_file'], 'w' )
	for g in globGraphList :
		globCycleList = []
		find_cycle_list( g )
		fh.write( '%s\n' % globCycleList )
	fh.close()


def write_to_db_file( sizeList ) :
	global globCycleList
	fh = open( os.path.join( fileDict['db_folder'], str( sizeList ) ), 'w' )
	fh.write( '%s\n' % ( len( globCurrGraphList ) + len( globDisconnectedGraphList ) ) )
	for g in globCurrGraphList :
		globCycleList = []
		find_cycle_list( g )
		fh.write( '%s\n' % globCycleList )
	for g in globDisconnectedGraphList :
		globCycleList = []
		find_cycle_list( g )
		fh.write( '%s\n' % globCycleList )
	fh.close()

# #########################################

def original_totality( sizeList ) :
	x, y, res = sum( sizeList ) - 1, globNode, 1
	for n in sizeList :
		res *= y ** x
		y -= 1
		x -= n
		if x <= 0 : break
	return res


def add_graph_attributes( g ) :
	g.vs['mult'] = 0
	edges = g.get_edgelist()
	sources = [ i for i, j in edges if i == j ]
	g.vs[sources]['mult'] = [ edges.count( ( p, p ) ) for p in sources ]
	g.es['mult'] = [ edges.count( ( e.source, e.target ) ) for e in g.es ]


def is_isomorphic( g1, g2 ) :
	return g1.isomorphic_vf2( g2, color1=g1.vs['mult'], color2=g2.vs['mult'], edge_color1=g1.es['mult'], edge_color2=g2.es['mult'] )


def not_isomorphic_graph( gr, connected=True ) :
	if connected == True :
		for g in globCurrGraphList :
			if is_isomorphic( gr, g ) :
				return False
	else :
		for g in globDisconnectedGraphList :
			if is_isomorphic( gr, g ) :
				return False
	return True


def delete_isomorphic_graphs() :
	for g in globGraphList :
		isoList = [ i for i, gr in enumerate( globCurrGraphList ) if is_isomorphic( g, gr ) ]
		isoList.reverse()
		for i in isoList :
			del globCurrGraphList[i]


def recur_add_loop( gr, curr, rest, fetch ) :
	if fetch == 1 :
		for p in rest :
			grNew = gr.copy()
			grNew.add_edges( list_to_edges( curr + [ p ] ) )
			add_graph_attributes( grNew )
			if not grNew.is_connected( mode=ig.WEAK ) :
				if not_isomorphic_graph( grNew, connected=False ) :
					globDisconnectedGraphList.append( grNew )
			elif not_isomorphic_graph( grNew ) :
				globCurrGraphList.append( grNew )
		return
	
	for p in range( len( rest ) ) :
		recur_add_loop( gr, curr + [ rest[p] ], rest[:p]+rest[p+1:], fetch-1 )


def gen_quivers() :
	global globCurrGraphList, globDisconnectedGraphList, globGraphList, globCycleList, fileDict
	
	lenSizeLists = calc_size_list()
	for count, sl in enumerate( globSizeLists ) :
		globCurrGraphList = []
		globDisconnectedGraphList = []
		output( '\n=== === === %s : %d // %d === === ===' % ( sl, count+1, lenSizeLists ) )
		output( 'ORIGINAL TOTALITY: {:,}\n------------------------------'.format( original_totality( sl ) ) )
		
		if is_primary( sl ) :
			output( 'BUILDING PRIMARY SIZE LIST...' )
			gr = ig.Graph( n=globNode, edges=list_to_edges( range( first_non_zero( sl ) + 1 ) ), directed=True )
			if gr.is_connected( mode=ig.WEAK ) :
				globCurrGraphList.append( gr )
			else :
				globDisconnectedGraphList.append( gr )
		else :
			rsl = reduce_size_list( sl )
			e = get_e_from_( rsl )
			dbFile = os.path.join( gen_file_dict( globNode, e )['db_folder'], str( rsl ) )
			
			if not check_file( dbFile ) :
				print '\nPlease generate <N=%d|E=%d>%s quiver database file first.\n' % ( globNode, e, rsl )
				my_quit( 2 )
			
			output( 'BUILDING FROM <N=%d|E=%d>...\n%s' % ( globNode, e, rsl ) )
			fh = open( dbFile, 'r' )
			totality = eval( fh.readline() )
			output( 'TOTALITY: {:,}\n------------------------------'.format( totality ) )
			for c, cycles in enumerate( fh ) :
				gr = make_graph_from_( globNode, eval( cycles ) )
				recur_add_loop( gr, [], range( globNode ), globEdge - e )
				if not (c+1) % 100 : output( 'DONE {:,} // {:,}.'.format( c+1, totality ) )
		
		output( '==== ==== ==== FOUND : %d GRAPH(S) ==== ==== ====\n' % len( globCurrGraphList ) )
		write_to_db_file( sl )
		delete_isomorphic_graphs()
		globGraphList += globCurrGraphList
	
	graphNumber = len( globGraphList )
	output( '_________________________________\nAll together found %d graph(s).' % graphNumber )
	if graphNumber :
		open( fileDict['count_file'], 'w' ).write( str( graphNumber ) )
		write_to_quiver_file()

# #########################################

def output_time( t ) :
	output( '_________________________________\nTakes %.3f second(s).' % t )
	if t > 60*60*24*5 :
		output( '~~ %.3f day(s).\n' % ( t/(60*60*24.0) ) )
	elif t > 60*60*10 :
		output( '~~ %.3f hour(s).\n' % ( t/(60*60.0) ) )
	elif t > 60*20 :
		output( '~~ %.3f minute(s).\n' % ( t/60.0 ) )
	print


if __name__ == '__main__' :
	os.chdir( os.path.join( os.getcwd(), os.path.dirname( __file__ ) ) )
	globNode, globEdge = wait_for_ne( sys.argv[1:] )
	fileDict = gen_file_dict( globNode, globEdge )
	check_folder( True, fileDict['root'], fileDict['n_folder'], fileDict['e_folder'], fileDict['db_folder'] )
	globOutputFile = open( fileDict['output_file'], 'w' )
	
	output( '\nVERSION: %s' % __version__ )
	output( '\n___ <N=%d|E=%d>' % ( globNode, globEdge ) )
	
	start = time.time()
	gen_quivers()
	output_time( time.time() - start )
	