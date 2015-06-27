# for import only

import sys
import os
import time

# #######################################

def my_quit( t=0 ) :
	time.sleep( t )
	sys.exit()


def wait_for_ne( args ) :
	try :
		n = int( args[0] )
		e = int( args[1] )
		return n, e
	except :
		print 'Give me N & E. E.g.:'
		print 'If N=2, E=4, please input: 2 4'
		ne = raw_input( 'Input: ' )
		ne = ne.strip().split( ' ' )
		try :
			n = int( ne[0] )
			e = int( ne[1] )
			return n, e
		except :
			print "\n!!! Invalid node & edge numbers. Quit..."
			my_quit( 1 )


def gen_file_dict( n, e ) :
	dict = {	'temp'	: 'TEMP',
			'root'	: 'DATA',
			'n'		: 'n=%s' % n,
			'e'		: 'e=%s' % e,
	}
	dict['scatter_file'] = os.path.join( dict['root'], 'scatter.txt' )
	dict['bg_scatter_file'] = os.path.join( dict['root'], 'bg_scatter.txt' )
	
	dict['n_folder'] = os.path.join( dict['root'], dict['n'] )
	dict['e_folder'] = os.path.join( dict['n_folder'], dict['e'] )
	dict['db_folder'] = os.path.join( dict['e_folder'], 'db' )
	
	dict['quiver_file'] = os.path.join( dict['e_folder'], 'quiver.txt' )
	dict['output_file'] = os.path.join( dict['e_folder'], 'output.txt' )
	dict['count_file'] = os.path.join( dict['e_folder'], 'count.txt' )
	
	dict['gio_folder'] = os.path.join( dict['e_folder'], 'gio' )
	dict['term_folder'] = os.path.join( dict['e_folder'], 'term' )
	dict['spot_folder'] = os.path.join( dict['e_folder'], 'spot' )
	dict['m2in_folder'] = os.path.join( dict['e_folder'], 'M2In' )
	dict['m2out_folder'] = os.path.join( dict['e_folder'], 'M2Out' )
	dict['present_folder'] = os.path.join( dict['e_folder'], 'present' )
	
	dict['spot_r_file'] = os.path.join( dict['spot_folder'], '%06d_r.txt' )
	dict['spot_file'] = os.path.join( dict['spot_folder'], '%06d.txt' )
	dict['term_file'] = os.path.join( dict['term_folder'], '%06d.txt' )
	dict['gio_file'] = os.path.join( dict['gio_folder'], '%06d.txt' )
	
	dict['m2in_file'] = os.path.join( dict['m2in_folder'], '%06d.m2' )
	dict['m2in_r_file'] = os.path.join( dict['m2in_folder'], '%06d_r.m2' )
	dict['m2out_file'] = os.path.join( dict['m2out_folder'], '%06d.txt' )
	dict['m2out_r_file'] = os.path.join( dict['m2out_folder'], '%06d_r.txt' )
	
	dict['present_file'] = os.path.join( dict['present_folder'], '%06d.txt' )
	dict['present_r_file'] = os.path.join( dict['present_folder'], '%06d_r.txt' )
	dict['dim_file'] = os.path.join( dict['e_folder'], 'dimension.txt' )
	dict['deg_file'] = os.path.join( dict['e_folder'], 'degree.txt' )
	dict['deg-dim_file'] = os.path.join( dict['e_folder'], 'deg-dim.txt' )
	dict['deg-dim_math_file'] = os.path.join( dict['e_folder'], 'deg-dim_math.txt' )
	
	# bg
	dict['bg_spot_folder'] = os.path.join( dict['e_folder'], 'bg_spot' )
	dict['bg_m2in_folder'] = os.path.join( dict['e_folder'], 'bg_M2In' )
	dict['bg_m2out_folder'] = os.path.join( dict['e_folder'], 'bg_M2Out' )
	dict['bg_present_folder'] = os.path.join( dict['e_folder'], 'bg_present' )
	
	dict['bg_spot_r_file'] = os.path.join( dict['bg_spot_folder'], '%06d_bg_r.txt' )
	dict['bg_spot_file'] = os.path.join( dict['bg_spot_folder'], '%06d_bg.txt' )
	
	dict['bg_m2in_file'] = os.path.join( dict['bg_m2in_folder'], '%06d_bg.m2' )
	dict['bg_m2in_r_file'] = os.path.join( dict['bg_m2in_folder'], '%06d_bg_r.m2' )
	dict['bg_m2out_file'] = os.path.join( dict['bg_m2out_folder'], '%06d_bg.txt' )
	dict['bg_m2out_r_file'] = os.path.join( dict['bg_m2out_folder'], '%06d_bg_r.txt' )
	
	dict['bg_present_file'] = os.path.join( dict['bg_present_folder'], '%06d_bg.txt' )
	dict['bg_present_r_file'] = os.path.join( dict['bg_present_folder'], '%06d_bg_r.txt' )
	dict['bg_dim_file'] = os.path.join( dict['e_folder'], 'bg_dimension.txt' )
	dict['bg_deg_file'] = os.path.join( dict['e_folder'], 'bg_degree.txt' )
	dict['bg_deg-dim_file'] = os.path.join( dict['e_folder'], 'bg_deg-dim.txt' )
	dict['bg_deg-dim_math_file'] = os.path.join( dict['e_folder'], 'bg_deg-dim_math.txt' )
	
	return dict


def check_folder( mkdir, *paths ) :
	val = True
	for path in paths :
		if not os.path.exists( path ) :
			val = False
			if mkdir == True :
				print 'Making new folder: %s'% path
				os.mkdir( path )

		elif not os.path.isdir( path ) :
			val = False
			if mkdir == True :
				print 'Removing file: %s' % path
				os.remove( path )
				print 'Making new folder with the same name.'
				os.mkdir( path )
	return val


def check_file( *paths ) :
	val = True
	for path in paths :
		if not os.path.exists( path ) :
			val = False
		elif not os.path.isfile( path ) :
			val = False
	return val


def list_to_edges( theList, closed=True ) :
	edges = [ ( theList[i], theList[i+1] ) for i in range( len( theList ) - 1 ) ]
	if closed == True :
		edges.append( ( theList[-1], theList[0] ) )
	return edges


def inner_prod( list1, list2 ) :
	return sum( [ list1[i] * list2[i] for i in range( min( len( list1 ), len( list2 ) ) ) ] )


def print_time( t ) :
	print '_________________________________\nTakes %.3f second(s).' % t
	if t > 60*60*24*5 :
		print '~~ %.3f day(s).\n' % ( t/(60*60*24.0) )
	elif t > 60*60*10 :
		print '~~ %.3f hour(s).\n' % ( t/(60*60.0) )
	elif t > 60*20 :
		print '~~ %.3f minute(s).\n' % ( t/60.0 )
	print

# #####################################

if __name__ == '__main__' :
	print '\nThis shared library is for import only.\n'
