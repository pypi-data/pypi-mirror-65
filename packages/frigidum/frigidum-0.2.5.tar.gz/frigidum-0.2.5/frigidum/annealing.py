import math
import random

from tqdm import tqdm, trange

def metropolis_acceptance(cost, new_cost, temperature):
	if new_cost < cost:
		return 1
	else:
		p = math.exp(- (new_cost - cost) / temperature)
		return p

"""

	Various Copy Strategies

"""

def copy(state):
	return state.copy()

def deepcopy(state):
	return state.deepcopy()

def naked(state):
	return state

"""

	Simulated Annealing Scheme

"""
def sa(	random_start,
		objective_function,
		neighbours,
		acceptance = metropolis_acceptance,
		T_start = 5,
		T_stop = 0.05,
		alpha = .9,
		repeats = 10**2,
		copy_state = copy,
		post_annealing = None):

	"""
	Simulated-Annealing Scheme, with tqdm
	
	Arguments:
		random_start: function which returns a random start / state
		objective_function: objective function to minimize
		neighbours: **list** of neighbor functions, for one use [neigh]
		T_start: Starting temperature
		T_stop: Stopping temperature
		alpha: lower temperature by this factor, after repeats proposals
		repeats: at each lowering by alpha, do repeats proposals
		copy = {'copy', 'deepcopy', 'naked'} - copy method
		post_annealing: function to call on state after annealing is finished.
	
	Output:
		T: Temperature (the lower, the less likely a proposal with increasing costs is accepted)
		M: Proportion of accepted states in last *repeats* proposals (Movements - keep moving when its cold)
		O_min: Minimum Objective Value found so far, in all previous states.
		O_current: Current Objective Value of last-accepted-state.
	
	"""
	state = random_start()
	cost = objective_function(state)

	best_found = copy_state(state)
	best_found_cost = cost

	T = T_start
	
	movements = 0
	
	coolings = int( math.ceil(  math.log(T_stop / T) / math.log(alpha)  ) )
	
	pbar = tqdm( range(coolings), unit='cooling' )

	neighbours_tried_stats = { k:0 for k in [ f.__name__ for f in neighbours] }
	neighbours_movement_stats = { k:0 for k in [ f.__name__ for f in neighbours] }
	

	for cooling in pbar:

		T = T * alpha
		movements_ratio = movements / repeats
		
		pbar.set_description("T: {:5.3f}, M: {:4.2f}, O_min: {:7.4f}, O_current: {:7.4f}".format(T,movements_ratio,best_found_cost,cost))
		
		movements=0

		for _ in range(repeats):
			
			random_neighbour = random.choice( neighbours )

			new_state = random_neighbour(state)
			new_cost = objective_function(new_state)

			neighbours_tried_stats[ random_neighbour.__name__ ] += 1
	
			if acceptance(cost, new_cost, T) > random.random():
				if new_cost != cost:
					movements += 1
					neighbours_movement_stats[ random_neighbour.__name__ ] += 1

				state, cost = copy_state(new_state), new_cost

			if cost < best_found_cost:
				best_found_cost = cost
				best_found = copy_state(state)

	if post_annealing:
		best_found = post_annealing(best_found)
		best_found_cost = objective_function(best_found)

	print("---")
	print("Neighbour Statistics: \n(proportion of proposals which got accepted *and* changed the objective function)")
	for neighbour in neighbours_tried_stats:
		print( "   {:32s} : {:5.3f}".format(neighbour[:31], (neighbours_movement_stats[neighbour]/neighbours_tried_stats[neighbour]) ))

	print("---")
	print("(Local) Minimum Objective Value Found: \n   {:.8f}".format(best_found_cost))

	return best_found, objective_function(best_found)