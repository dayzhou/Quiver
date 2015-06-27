#! /usr/bin/env python

r"""
Generate data files for M2 to calculate
"""

__version__ = '0.0.2'

import sys
import os
import time
import math
from share import *
from random import randrange as random_number
from itertools import combinations as combi
import sympy as sym

# #####################################

globNode = 0
globEdge = 0

globCycles = []

globGIOList = []
globShortGIOList = []

globSampleSize = 500

globBaseNumber = 11
globJointCharTuple = ( '', '+', '+2', '+3', '+4', '+5', '-5', '-4', '-3', '-2', '-' )
globJointCoeffTuple = ( 0, 1, 2, 3, 4, 5, -5, -4, -3, -2, -1 )

# #####################################

def cycles_to_edges( cycles ) :
	edges = []
	for list in cycles :
		edges += list_to_edges( list, closed=False )
	return edges


def label_edges( edges ) :
	labeledEdges = []
	for i, e in enumerate( edges ) :
		labeledEdges.append( [ e[0], e[1], edges[:i].count( e ) + 1 ] )
	return labeledEdges


def find_adj_edges( edges, trail ) :
	adj = []
	for e in edges :
		if e[0] == trail[-1][1] and e not in trail :
			adj.append( e )
	return adj


def is_equiv_cycle( cycle, cyclesList ) :
	rotateList = [ cycle[i:] + cycle[:i] for i in range( len( cycle ) ) ]
	for c in cyclesList :
		if len( c ) == len( cycle ) and c in rotateList :
			return True
	return False


def recur_find_cycles( edges, trail ) :
	if trail[-1][1] == trail[0][0] and not is_equiv_cycle( trail, globCycles ) :
		globCycles.append( trail )
	
	for e in find_adj_edges( edges, trail ) :
		recur_find_cycles( edges, trail+[e] )


def find_all_cycles( edges ) :
	global globCycles
	globCycles = []
	for e in edges :
		recur_find_cycles( edges, [e] )

# #####################################

def select_Ws( cycles ) :
	return [ c for c in cycles if len( c ) > 2 ]


def trail_of_cycle( cycle ) :
	trail = [ cycle[0][0] ]
	for e in cycle :
		if e[1] != trail[-1] :
			trail.append( e[1] )
	if len( trail ) > 1 :
		del trail[-1]
	return trail


def is_minimal_cycle( cycle ) :
	trail = trail_of_cycle( cycle )
	for p in trail :
		if trail.count( p ) > 1 :
			return False
	return True


def all_non_empty_subsets( set ) :
	subs = []
	for i in range( len( set ) ) :
		subs += [ list( s ) for s in combi( set, i+1 ) ]
	return subs


def select_GIOs( cyclesList ) :
	selfLoops = [ c[0] for c in cyclesList if len( c ) == 1 ]
	
	minCycles = []
	for cycle in [ c for c in cyclesList if len( c ) > 1 ] :
		newCycle = [ e for e in cycle if e[0] != e[1] ]
		if newCycle and is_minimal_cycle( newCycle ) and not is_equiv_cycle( newCycle, minCycles ) :
			minCycles.append( newCycle )
	
	allCycles = minCycles[:]
	for cycle in minCycles :
		loopsOnCycle = [ loop for loop in selfLoops if loop[0] in trail_of_cycle( cycle ) ]
		for subset in all_non_empty_subsets( loopsOnCycle ) :
			allCycles.append( cycle + subset )
	
	return allCycles

# #####################################

def edge_to_expr( edge ) :
	if edge[0] == edge[1] :
		return 'Superscript[Subscript[\\[Phi], %d], %d]' % ( edge[0]+1, edge[2] )
	return 'Superscript[Subscript[x, %d, %d], %d]' % ( edge[0]+1, edge[1]+1, edge[2] )


"""
def write_to_wterm_file( wList, k ) :
	fh = open( fileDict['bg_term_file'] % k, 'w' )
	for cycle in wList :
		fh.write( '{%s}\n' % ', '.join( [ edge_to_expr( e ) for e in cycle ] ) )
	fh.close()


def write_to_gio_file( k ) :
	fh = open( fileDict['bg_gio_file'] % k, 'w' )
	for cycle in globGIOList :
		fh.write( '{%s}\n' % ', '.join( [ edge_to_expr( e ) for e in cycle ] ) )
	fh.close()
"""
# #####################################

def to_digits( num ) :
	digits = []
	while num :
		digits.append( num % globBaseNumber )
		num //= globBaseNumber
	return digits


def to_complement_digits( coeffs ) :
	return [ c and ( globBaseNumber - c ) for c in coeffs ]


def to_number( coeffs ) :
	return sum( [ c * globBaseNumber ** i for i, c in enumerate( coeffs ) ] )


def wterm_to_expr( tempList, coeffs ) :
	wterm = ''
	for i, c in enumerate( coeffs ) :
		if c :
			wterm = globJointCharTuple[c].join( [ wterm, '*'.join( [ edge_to_expr( e ) for e in tempList[i] ] ) ] )
	return '%s\n' % wterm


def edge_to_var( edge ) :
	return 'X_%d_%d_%d' % ( edge[0]+1, edge[1]+1, edge[2] )


def gio_list_to_var_expr( gioList ) :
	return map( lambda cycle : map( edge_to_var, cycle ), gioList )


def get_all_variables( gioVarList ) :
	variables = []
	for cycle in gioVarList :
		for var in cycle :
			if var not in variables :
				variables.append( var )
	return variables


def gen_m2_input( gios, fterms, variables ) :
	for i, v in enumerate( variables ) :
		gios = gios.replace( v, 'X_{%d}' % (i+1) )
		fterms = fterms.replace( v, 'X_{%d}' % (i+1) )
	gios = gios.replace( '[', '{' ).replace( ']', '}' )
	fterms = fterms.replace( '[', '{' ).replace( ']', '}' )

	return	'R=ZZ/101[X_{1}..X_{' + str( len( variables ) ) + '}];\n' + \
			'S=ZZ/101[y_{1}..y_{' + str( len( globGIOList ) ) + '}];\n' + \
			'dterms = ' + gios + ';\n' + \
			'fterms = ' + fterms + ';\n' + \
			'fterms = trim ideal fterms;\n' + \
			'fterms = intersect decompose fterms;\n' + \
			'V = ker map(R/fterms,S,dterms);\n' + \
			'\n'


def all_potentials( k ) :
	gios = gio_list_to_var_expr( globGIOList )
	variables = get_all_variables( gios )
	sym.var( variables )
	
	gios = map( lambda cycle : map( eval, cycle ), gios )
	giosShort = map( lambda cycle : reduce( lambda x, y : x * y, cycle ), [ c for c in gios if len( c ) > 2 ] )
	gios = str( map( lambda cycle : reduce( lambda x, y : x * y, cycle ), gios ) )
	
	index, wList = 0, ''
	fh = open( fileDict['bg_m2in_file'] % k, 'w' )
	for i in range( 1, globBaseNumber ** len( globBigGIOList ) ) :
		coeffs = to_digits( i )
		if to_number( to_complement_digits( coeffs ) ) > i :
			index += 1
			w = inner_prod( [ globJointCoeffTuple[c] for c in coeffs ], giosShort )
			fterms = str( map( w.diff, variables ) )
			fh.write( gen_m2_input( gios, fterms, variables ) )
			wList += wterm_to_expr( globBigGIOList, coeffs )
	
	if wList :
		open( fileDict['bg_spot_file'] % k, 'w' ).write( wList )
	return index


def random_potentials( k ) :
	gios = gio_list_to_var_expr( globGIOList )
	variables = get_all_variables( gios )
	sym.var( variables )
	
	gios = map( lambda cycle : map( eval, cycle ), gios )
	giosShort = map( lambda cycle : reduce( lambda x, y : x * y, cycle ), [ c for c in gios if len( c ) > 2 ] )
	gios = str( map( lambda cycle : reduce( lambda x, y : x * y, cycle ), gios ) )
	
	index, samples, wList = 0, [], ''
	fh = open( fileDict['bg_m2in_r_file'] % k, 'w' )
	while index < globSampleSize :
		rand = random_number( 1, globBaseNumber ** len( globBigGIOList ) )
		coeffs = to_digits( rand )
		if rand in samples or to_number( to_complement_digits( coeffs ) ) in samples :
			continue
		index += 1
		
		w = inner_prod( [ globJointCoeffTuple[c] for c in coeffs ], giosShort )
		fterms = str( map( w.diff, variables ) )
		fh.write( gen_m2_input( gios, fterms, variables ) )
		wList += wterm_to_expr( globBigGIOList, coeffs )
	
	if wList :
		open( fileDict['bg_spot_r_file'] % k, 'w' ).write( wList )
	return index


def handle_potentials( k ) :
	length = len( globBigGIOList )
	print 'Length of GIO Short List: %d' % length	
	
	if length <= int( math.floor( math.log( 2*globSampleSize+1, globBaseNumber ) ) ) :
		print 'Number of SuperPotentials: %d' % all_potentials( k )
	else :
		print 'PROCESSING RANDOM SAMPLING...'
		print 'Number of SuperPotentials: %d' % random_potentials( k )

	
# #####################################

def gen_data_files() :
	global globGIOList, globBigGIOList
	for count, cycles in enumerate( open( fileDict['quiver_file'], 'r' ) ) :
		print '\n=== === PROCESSING GRAPH: %d === ===' % ( count+1 )
		edges = label_edges( cycles_to_edges( eval( cycles ) ) )
		find_all_cycles( edges )
		
		globGIOList = select_GIOs( globCycles )
		globBigGIOList = [ c for c in globGIOList if len( c ) > 2 ]
		handle_potentials( count+1 )

# #####################################

if __name__ == '__main__' :
	os.chdir( os.path.join( os.getcwd(), os.path.dirname( __file__ ) ) )
	print '\nVERSION: %s\n' % __version__
	
	globNode, globEdge = wait_for_ne( sys.argv[1:] )
	fileDict = gen_file_dict( globNode, globEdge )
	
	if not check_file( fileDict['quiver_file'] ) :
		print 'The quiver file does not exist. Quit...'
		my_quit( 2 )
	check_folder( True, fileDict['bg_spot_folder'], fileDict['bg_m2in_folder'], fileDict['bg_m2out_folder'] )
	
	start = time.time()
	gen_data_files()
	print_time( time.time() - start )
	