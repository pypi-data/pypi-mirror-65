# Simmulated Annealing package for Python

## Installation

```
pip install frigidum
```

## Example Usage

```
import frigidum

import random

def random_start():
    return 50 + random.random()

def random_small_step(x):
    return x + 0.1 * (random.random() - .5)

def random_big_step(x):
    return x + 10 * (random.random() - .5)

def obj(x):
    return x**2
    
local_opt = frigidum.sa(random_start=random_start, random_neighbours=[random_small_step, random_big_step], cost_function=obj, T_start=100, T_stop = 0.001, repeats=10**4, copy_state=frigidum.annealing.naked)
```

Arguments:
 - `random_start`: function which returns a random start / state
 - `cost_function`: objective function to minimize
 - `random_neighbours`: list of neighbor functions
 - `t_start`: Starting temperature
 - `T_stop`: Stopping temperature
 - `alpha`: lower temperature by this factor, after repeats proposals
 - `repeats`: at each lowewing by alpha, do repeats proposals
 - `copy` = {'copy', 'deepcopy', 'naked'} - copy method


## Movements

A movement is a when a proposed state is accepted, and the objective function has changed. For each batch of repeats, the proportion of movements are displayed.

In the early phase of annealing, movements should happen >90%.

In the last phase of annealing, movements should happen <5%.

## Copy'ing of States

3 most important copy methods are included in the `annealing` module,

```
def copy(state):
	return state.copy()

def deepcopy(state):
	return state.deepcopy()

def naked(state):
	return state
```

In the example, `naked` with the argument `copy_state=frigidum.annealing.naked` is used.

## To-Do:

- Statistics of acceptance of various movements/neighbors
- Multitreadding (N simultanous anneals)
- Drilling (after repeats, re-repeat with low temp)
- Re-Annealing
- Auto-set start Tempreature (Based on >90% movemenets)
- Auto-stop (Based on near 0 movemebts)
