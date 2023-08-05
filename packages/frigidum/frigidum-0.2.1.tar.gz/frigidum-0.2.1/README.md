# Simulated Annealing package for Python, using tqdm

![frigidum](https://gitlab.com/whendrik/frigidum/-/raw/master/images/frigidum_0.9.1.gif)

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

local_opt = frigidum.sa(random_start=random_start, 
                        neighbours=[random_small_step, random_big_step], 
                        objective_function=obj, 
                        T_start=100, 
                        T_stop=0.000001, 
                        repeats=10**4, 
                        copy_state=frigidum.annealing.naked)
```

Arguments:
 - `random_start` : function which returns a random start / state.
 - `objective_function` : objective function to minimize.
 - `neighbours` : **list** of neighbor functions, for one use [func]. For each proposal, a neighbour is randomly selected (equal weights).
 - `T_start` : Starting temperature.
 - `T_stop` : Stopping temperature.
 - `alpha` : lower temperature by this factor, after repeats proposals.
 - `repeats` : at each lowering by alpha, do repeats proposals.
 - `copy`  = `frigidum.annealing.copy`, `frigidum.annealing.deepcopy`, `frigidum.annealing.naked`, or custom - the copy method.


## Movements

A movement is a when a proposed state is accepted, and the objective function has changed. For each batch of repeats, the proportion of movements are displayed.

- In the early phase of annealing, movements should happen >90%.

- In the last phase of annealing, movements should happen <10%.

Movements are useful to determine the starting- and stopping temperature; `T_start` & `T_stop`, with the above guidelines.

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

In the example, `naked` with the argument `copy_state=frigidum.annealing.naked` is used,

- use `copy_state=frigidum.annealing.copy` for `copy()`,
- use `copy_state=frigidum.annealing.deepcopy` for `deepcopy()`,
- use `copy_state=frigidum.annealing.naked` if `a = b` would already create a copy.

## General Advise with Simulated Annealing

- Focus on the neighbour function, not the cooling scheme or acceptance variations.
- To get inspiration for random neighbours, try solve a similar problem yourself.
- Try multiple neighbours together, combinations usually work well. The `neighbours` argument expects a list of neighbours.
- Try add neighbours, that might work well when cold.
- Try add neighbours, that might work well when warm.
- Try add neighbours, that find a local minima with local greedy algorithm.
- It is difficult to predict the effect of random neighbour, usually my ideas don't survive the outcome of experiments.
- When conditions apply, stay within the feasible zone when possible.


## To-Do:

- Multitreadding (N simultanous anneals)
- Drilling (after repeats, re-repeat with low temp)
- Re-Annealing
- Auto-set start Tempreature (Based on >90% movemenets)
- Auto-stop (Based on near 0 movements)
