import math
import random

from tqdm import tqdm

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
		copy_state = copy):

	"""
	Simulated-Annealing Scheme, with tqdm
	
	Arguments:
		random_start: function which returns a random start / state
		objective_function: objective function to minimize
		neighbours: **list** of neighbor functions, for one use [neigh]
		t_start: Starting temperature
		T_stop: Stopping temperature
		alpha: lower temperature by this factor, after repeats proposals
		repeats: at each lowering by alpha, do repeats proposals
		copy = {'copy', 'deepcopy', 'naked'} - copy method
	
	Output:
		T: Temperature (the lower, the less likely a proposal with increasing costs is accepted)
		M: Proportion of accepted states in last *repeats* proposals (Movements - keep moving when its cold)
		C_min: Minimum Objective Value found so far, in all previous states
		C_current: Current Objective Value of last-accepted-state
	
	"""
	state = random_start()
	cost = objective_function(state)

	best_found = copy_state(state)
	best_found_cost = cost

	T = T_start
	
	movements = 0
	
	coolings = int( math.ceil(  math.log(T_stop / T) / math.log(alpha)  ) )
	
	pbar = tqdm( range(coolings), unit='cooling' )
	
	for cooling in pbar:

		T = T * alpha
		movements_ratio = movements / repeats
		
		pbar.set_description("T: {:5.3f}, M: {:4.2f}, C_min: {:7.4f}, C_current: {:7.4f}".format(T,movements_ratio,best_found_cost,cost))
		
		movements=0

		for _ in range(repeats):
			
			random_neighbour = random.choice( neighbours )

			new_state = random_neighbour(state)
			new_cost = objective_function(new_state)
	
			if acceptance(cost, new_cost, T) > random.random():
				if new_cost != cost:
					movements += 1

				state, cost = copy_state(new_state), new_cost

			if cost < best_found_cost:
				best_found_cost = cost
				best_found = copy_state(state)
					
	print("---")
	print("Best Found Cost: {:.8f}".format(best_found_cost))
	return best_found, objective_function(best_found)