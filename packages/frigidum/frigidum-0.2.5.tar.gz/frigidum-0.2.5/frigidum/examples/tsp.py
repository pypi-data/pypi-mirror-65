"""

Benchmark Examples For the TSP Problem taken from 

http://elib.zib.de/pub/mp-testdata/tsp/tsplib/tsp/

"""


"""
import frigidum

from frigidum.examples import tsp

local_opt = frigidum.sa(random_start=tsp.random_start,
           objective_function=tsp.objective_function,
           neighbours=[euclidian_bomb_and_fix, route_bomb_and_fix, random_disconnect_vertices_and_fix],
           copy_state=frigidum.annealing.naked,
           T_start=10**3,
           T_stop=0.001,
           repeats=10**2,
           post_annealing = local_search_2opt)
"""
import os
import inspect
import re
import frigidum

import numpy as np


FRIGIDUM_PATH = os.path.dirname(inspect.getfile(frigidum))
TSPLIB_PATH = FRIGIDUM_PATH + '/examples/tsplib/'

"""
	REGEX taken from https://www.regular-expressions.info/floatingpoint.html

	Needed to parse the .tsp format from tsplib
"""
re_node_line = re.compile("(\d+) ([0-9]*\.?[0-9]+)([eE][-+]?[0-9]+)? ([0-9]*\.?[0-9]+)([eE][-+]?[0-9]+)?")
nodes_dict = {}
pcb442_path = TSPLIB_PATH + 'pcb442.tsp'

"""

	Parse the .tsp file in TSPLIB format

"""

with open(pcb442_path) as f:
	for line in f:
		result = re_node_line.match(line)
		if result:
			node_id = int(result.group(1))
			
			x_coord = float(result.group(2) + result.group(3))
			y_coord = float(result.group(4) + result.group(5))

			nodes_dict[ node_id ] = (x_coord, y_coord)

nodes_count = max(nodes_dict.keys())
nodes = np.zeros( (nodes_count,2) )

for k in nodes_dict:
	nodes[k-1] = np.array( nodes_dict[k] )

"""
	Calculate the distance matrix

	dist_sq = squared
	dist_eu = Euclidian Distance between 2 points in 2-D space
"""

dist_sq = np.sum((nodes[:, np.newaxis, :] - nodes[np.newaxis, :, :]) ** 2, axis = -1)
dist_eu = np.sqrt(dist_sq)


def random_start():
	"""
		Random start
	"""
	a = np.arange(0,nodes_count)
	np.random.shuffle(a)
	return a

def check_all_nodes_visited(route):
	"""
		Check is a solution is valid;
		- No double nodes
		- Each node visited
	"""
	return np.all( np.sort(route) == np.arange(0,nodes_count) ) 

def objective_function( route ):
	#assert check_all_nodes_visited(route)

	route_shifted = np.roll(route,1)
	return 	np.sum( dist_eu[route,route_shifted] )

def random_swap( route ):
	"""
		Random Swap - a Naive neighbour function

		Will only work for small instances of the problem
	"""
	route_copy = route.copy()

	random_indici = np.random.choice( route , 2, replace = False)
	route_copy[ random_indici[0] ] = route[ random_indici[1] ]
	route_copy[ random_indici[1] ] = route[ random_indici[0] ]

	return route_copy

def vertex_insert( route, nodes=1 ):
	"""
		Vertex Insert Neighbour, inspired by

		http://www.sciencedirect.com/science/article/pii/S1568494611000573
	"""
	route_copy = route.copy()
	random_indici = np.random.choice( route , 2, replace = False)
	index_of_point_to_reroute = random_indici[0]
	value_of_point_to_reroute = route[ random_indici[0] ]
	index_of_new_place = random_indici[1]
	route_copy = np.delete(route_copy, index_of_point_to_reroute)
	route_copy = np.insert(route_copy, index_of_new_place, values=value_of_point_to_reroute)
	return route_copy

def block_reverse( route, nodes=1 ):
	"""
		Block Reverse Neighbour, inspired by

		http://www.sciencedirect.com/science/article/pii/S1568494611000573
	"""
	route_copy = route.copy()
	random_indici = np.random.choice( route , 2, replace = False)
	index_of_cut_left = np.min(random_indici)
	index_of_cut_right = np.max(random_indici)
	route_copy[ index_of_cut_left:index_of_cut_right ] = np.flip(route_copy[ index_of_cut_left:index_of_cut_right ])

	return route_copy

def euclidian_bomb_and_fix( route ):
	"""
		Randomly Disconnects nodes (set to -1),
		based on a 'bomb', exploded on random node with radius.

		After damange of bomb, it will re-connect all affected
		nodes with a fixing method.

	"""
	bombed_route = route.copy()

	random_index = np.random.choice( route )

	max_radius = np.max(dist_eu)
	max_vertices_to_bomb = 20
	radius = np.random.exponential( max_radius / 10)

	"""
		Disconnect all vertices inside radius of bomb (set to -1)
	"""
	vertices_to_disconnect = np.argwhere( dist_eu[random_index] < radius )

	do = dist_eu[random_index,vertices_to_disconnect].T[0].argsort()   
	vertices_to_disconnect = vertices_to_disconnect[do]
	vertices_to_disconnect = vertices_to_disconnect[:max_vertices_to_bomb]

	indices_to_disconnect = np.argwhere( route == vertices_to_disconnect )[:,1]

	bombed_route[  indices_to_disconnect ] = -1


	"""
		(Randomly?) Select fixing mechanism
	"""
	if np.random.random() > .5 :
		return stochastic_greedy_glue_missing(bombed_route)
	else:
		return stochastic_greedy_reroute_missing(bombed_route)


def route_bomb_and_fix( route ):
	"""
		Randomly Disconnects nodes (set to -1),
		based on a 'route bomb';

		It randomly disconnect a chain of N nodes.

		After damange of bomb, it will re-connect all affected
		nodes with a fixing method.

	"""

	bombed_route = route.copy()
	
	random_index = np.random.choice( route )

	length_of_bomb = 1 + np.random.poisson( 12 ) 

	bombed_route[ random_index:random_index+length_of_bomb] = -1

	if random_index+length_of_bomb > route.size:
		bombed_route[ :( (random_index+length_of_bomb) % route.size )] = -1

	"""
		Disconnect chain starting from selected vertex with length
	"""

	"""
	 	randomly select fixing mecnism
	"""
	if np.random.random() > .3 :
		return stochastic_greedy_glue_missing(bombed_route)
	else:
		return stochastic_greedy_reroute_missing(bombed_route)


def random_disconnect_vertices_and_fix( route ):
	"""
		Randomly Disconnects K nodes (set to -1),

		After damange of bomb, it will re-connect all affected
		nodes with a fixing method.

	"""

	bombed_route = route.copy()

	size_of_bomb = 1 + np.random.poisson( 12 )

	random_indices = np.random.choice( route , size_of_bomb, replace = False)

	bombed_route[ random_indices ] = -1

	return stochastic_greedy_reroute_missing(bombed_route)


def stochastic_glue_enpoints( list_of_route_parts ):
	"""
		Check if N=1
	"""
	if len(list_of_route_parts) < 2:
		return list_of_route_parts

	"""
		End-points
	"""
	end_points_with_duplicated = np.array( [ [r[0],r[-1]] for r in list_of_route_parts])
	end_points = np.unique(end_points_with_duplicated.flatten() )

	"""
		Create pair-distance-matrix
	"""

	pair_distances = dist_eu[ end_points.reshape(-1,1),end_points  ] 


	"""
		Select Upper/Lower Triag & 
		Select minimum pair
	"""

	pair_size = pair_distances.shape[0]

	tril_indices = np.tril_indices( pair_distances.shape[0] ,-1)
	np_tril_indices = np.array(tril_indices)

	unscaled_weights = pair_distances[ tril_indices ]

	uw_max = np.max(unscaled_weights)
	uw_min = np.min(unscaled_weights)
	transformed_weights = uw_max - unscaled_weights + (uw_min/100)
	transformed_weights = transformed_weights / np.max(transformed_weights)

	stretched_weights = transformed_weights ** 50


	"""
		Set own head/tail weights to 0
	"""

	own_up = [np.argwhere(end_points == a[0])[0][0] for a in end_points_with_duplicated]
	own_down = [np.argwhere(end_points == a[1])[0][0] for a in end_points_with_duplicated]
	to_zero = np.array( [own_down,own_up] )

	to_zero_index_arg = [ np.argwhere( np.all(np_tril_indices.T == z ,axis=1 )) for z in to_zero.T]
	to_zero_index = [z[0][0] for z in to_zero_index_arg if z.size > 0 ]

	to_zero_index_arg_flip = [ np.argwhere( np.all(np_tril_indices.T == np.flip(z) ,axis=1 )) for z in to_zero.T]
	to_zero_index_flip = [z[0][0] for z in to_zero_index_arg_flip if z.size > 0 ]

	np_to_zero = np.array(to_zero_index + to_zero_index_flip)

	if np_to_zero.size > 0:
		stretched_weights[ np_to_zero ] = 0

	"""
		Finally weights
	"""
	weights = stretched_weights / np.sum( stretched_weights )

	if np.isnan(weights).any():
		print(weights)
		print("----")
		print(list_of_route_parts)
		print(pair_distances)
		print(unscaled_weights)
		print("+++++++++++++")
		print(transformed_weights)
		print(stretched_weights)
		print("+++++++++++++")


	pair_index = np.random.choice( np.arange(tril_indices[0].size) , p=weights)
	
	endpoint_index_left =  tril_indices[0][pair_index]
	endpoint_index_print =  tril_indices[1][pair_index] 

	pair = end_points[endpoint_index_left], end_points[endpoint_index_print]

	"""
		Glue Pair together
	"""

	parts_to_glue = [ part for part in list_of_route_parts if (pair[0] in part) or (pair[1] in part) ]
	parts_to_glue_ordered = [p if pair[0] == p[0] or pair[1] == p[0] else np.flip(p) for p in parts_to_glue]

	glued_part = np.concatenate( [np.flip(parts_to_glue_ordered[0]), parts_to_glue_ordered[1] ])

	"""
		Remainings
	"""

	left_overs = [part for part in list_of_route_parts if pair[0] not in part and pair[1] not in part]


	"""
		Recursion
	"""

	return stochastic_glue_enpoints( left_overs + [glued_part] )


def stochastic_greedy_glue_missing( broken_route ):
	"""
		Greedy fix (small distances have higher chance),
		a broken route.

		It wil re-connect all broken parts/nodes, 
		by chance, but smaller distances have higher 
		probability to be picked as fix.
	"""

	complete_nodes = np.arange(broken_route.size)
	missing_nodes = np.delete(complete_nodes, broken_route[ broken_route > -1] )


	if missing_nodes.size == broken_route.size:
		broken_route[0] = 0
		missing_nodes = missing_nodes[1:]

	"""
		Split: 
		https://stackoverflow.com/questions/38277182/splitting-numpy-array-based-on-value

	"""

	missing_idx = np.where(broken_route != -1)[0]
	list_of_parts = np.split(broken_route[missing_idx],np.where(np.diff(missing_idx)!=1)[0]+1)

	"""
		Call Helper Function		
	"""

	missing_parts = [ np.array([m]) for m in missing_nodes]

	
	return stochastic_glue_enpoints( list_of_parts +  missing_parts )[0]


def stochastic_reroute_missing( incomplete_route, missing_vertices ):

	while missing_vertices.size > 0:

		dist_to = dist_eu[missing_vertices.reshape(-1,1), incomplete_route]
		dist_return = dist_eu[missing_vertices.reshape(-1,1), np.roll(incomplete_route,-1)]

		dist_reroute = dist_to + dist_return

		uw_max = np.max(dist_reroute)
		uw_min = np.min(dist_reroute)
		transformed_weights = uw_max - dist_reroute + (uw_min/100)
		transformed_weights = transformed_weights / np.max(transformed_weights)

		stretched_weights = transformed_weights ** 150


		weights = stretched_weights / np.sum(stretched_weights)

		flat_index = np.random.choice( np.arange(weights.size), p=weights.flatten() )
		index = np.unravel_index( flat_index, weights.shape)

		
		incomplete_route = np.insert(incomplete_route, index[1], values=missing_vertices[index[0]])
		missing_vertices = np.delete(missing_vertices, index[0])
		

	return incomplete_route

def stochastic_greedy_reroute_missing( broken_route ):
	"""
		Greedy fix (small distances have higher chance),
		a broken route.

		It wil first create a small cycle sub-route.
		This is a complete_route.

		For all remaining missing nodes, it will add them
		to the route, by inserting them (reroute).

		The selection process is based on chance,
		but smaller reroute have higher chance to be picked.
	"""

	complete_nodes = np.arange(broken_route.size)
	missing_nodes = np.delete(complete_nodes, broken_route[ broken_route > -1] )

	if missing_nodes.size == broken_route.size:
		broken_route[0] = 0
		missing_nodes = missing_nodes[1:]

	"""
		Split: 
		https://stackoverflow.com/questions/38277182/splitting-numpy-array-based-on-value

	"""

	missing_idx = np.where(broken_route != -1)[0]
	list_of_parts = np.split(broken_route[missing_idx],np.where(np.diff(missing_idx)!=1)[0]+1)

	incomplete_route = stochastic_glue_enpoints(list_of_parts)[0]

	"""
		for vertex in missing_nodes, reroute ass in incomplete_route
	"""
	complete_route = stochastic_reroute_missing(incomplete_route, missing_nodes)


	return complete_route


def swap_for_2opt( route, i, k):
	"""
		Helper for 2-opt search
	"""
	route_copy = route.copy()
	index_of_cut_left = i
	index_of_cut_right = k
	route_copy[ index_of_cut_left:index_of_cut_right ] = np.flip(route_copy[ index_of_cut_left:index_of_cut_right ])

	return route_copy

def local_search_2opt( route ):
	"""
		Local Optimum with 2-opt

		https://en.wikipedia.org/wiki/2-opt
		
	"""
	steps_since_improved = 0
	still_improving = True

	route = route.copy()

	while still_improving :
		for i in range( route.size - 1 ):
			for k in np.arange( i + 1, route.size ):
				alt_route = swap_for_2opt(route, i, k)

				if objective_function(alt_route) < objective_function(route):
					route = alt_route.copy()
					steps_since_improved = 0

			steps_since_improved += 1

			if steps_since_improved > route.size + 1:
				still_improving = False
				break

	return route



opt_sol = np.array([ 0,	1,	2,	3,	4,	5, 6, 7, 8, 9, 10, 11, 12,
		13, 14, 15, 16, 17, 18, 19, 52, 51, 50, 82, 83, 84,
		380, 381, 85, 53, 20, 21, 54, 86, 377, 87, 55, 22, 23,
		24, 25, 26, 27, 28, 29, 30, 31, 375, 376, 32, 64, 63,
		62, 61, 60, 59, 58, 57, 56, 88, 89, 90, 91, 92, 100,
		110, 122, 132, 145, 157, 168, 181, 196, 195, 194, 193, 180, 167,
		156, 144, 143, 390, 131, 121, 109, 120, 384, 108, 119, 387, 130,
		142, 155, 166, 179, 192, 191, 203, 215, 224, 232, 407, 408, 411,
		412, 403, 216, 204, 205, 206, 207, 217, 218, 208, 197, 182, 169,
		158, 146, 133, 123, 111, 435, 93, 94, 378, 95, 379, 96, 97,
		383, 382, 112, 124, 134, 147, 159, 170, 183, 198, 209, 219, 225,
		410, 409, 413, 236, 264, 436, 274, 422, 437, 271, 419, 267, 415,
		263, 235, 262, 261, 260, 421, 418, 259, 258, 257, 256, 255, 254,
		253, 252, 417, 416, 251, 250, 249, 414, 248, 247, 246, 245, 244,
		243, 242, 241, 240, 406, 227, 234, 239, 266, 270, 269, 273, 276,
		425, 279, 439, 307, 308, 282, 283, 309, 338, 310, 284, 285, 311,
		339, 312, 286, 287, 313, 314, 315, 289, 288, 423, 420, 424, 290,
		316, 317, 291, 292, 318, 319, 293, 294, 320, 321, 295, 277, 296,
		322, 429, 428, 323, 297, 298, 299, 324, 325, 300, 301, 326, 327,
		302, 303, 328, 329, 304, 305, 330, 331, 332, 431, 333, 306, 334,
		335, 426, 336, 337, 374, 373, 372, 371, 370, 369, 368, 367, 344,
		366, 365, 364, 430, 363, 362, 361, 343, 360, 359, 358, 434, 357,
		356, 355, 433, 354, 353, 352, 342, 351, 350, 349, 348, 432, 347,
		346, 345, 341, 340, 427, 281, 280, 278, 275, 272, 268, 265, 238,
		237, 233, 226, 404, 405, 400, 399, 184, 171, 160, 148, 135, 125,
		113, 102, 101, 440, 103, 114, 385, 126, 386, 388, 115, 137, 391,
		151, 150, 136, 149, 161, 172, 185, 173, 395, 398, 186, 174, 210,
		402, 220, 228, 211, 229, 221, 212, 199, 187, 175, 162, 392, 152,
		138, 139, 127, 116, 104, 105, 106, 117, 128, 140, 153, 164, 163,
		396, 176, 188, 200, 201, 401, 213, 222, 230, 231, 223, 214, 202,
		189, 190, 397, 177, 178, 394, 393, 165, 154, 141, 389, 129, 118,
		107, 438, 81, 49, 48, 80, 99, 79, 47, 46, 78, 77, 45,
		44, 76, 98, 75, 43, 42, 74, 73, 41, 40, 72, 71, 39,
		38, 70, 69, 37, 36, 68, 67, 35, 34, 66, 65, 33, 441])
