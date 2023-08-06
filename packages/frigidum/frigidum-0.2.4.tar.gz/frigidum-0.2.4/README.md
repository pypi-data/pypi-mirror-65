# Simulated Annealing package for Python, using tqdm

![frigidum](https://gitlab.com/whendrik/frigidum/-/raw/master/images/frigidum_0.2.2.gif)

## Installation

```
pip install frigidum
```

## Basic Example Usage

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

### Arguments:

 - `random_start` : function which returns a random start / state.
 - `objective_function` : objective function to minimize.
 - `neighbours` : **list** of neighbour functions, for one use [neighbour]. For each proposal, a neighbour is randomly selected (equal weights).
 - `T_start` : Starting temperature.
 - `T_stop` : Stopping temperature.
 - `alpha` : Lower temperature by this factor, after repeats proposals.
 - `repeats` : at each temperature lowering by factor `alpha`, do repeats proposals.
 - `copy`  = `frigidum.annealing.copy`, `frigidum.annealing.deepcopy`, `frigidum.annealing.naked`, or custom - the copy method.

### Output & Return

- During a run, `print` Temperate `T`, Movements proportion in current batch of repeats `M`, minimum Objective found so far `O_min`, last-accepted Objective value `O_current`, and various progress information provided by `tqdm`.
- At the end, `print` movement statistics of neighbours used.
- returns a `(best_found_state, objective_function(best_found_state) )` tuple when done.

## Movements

A movement is a when a proposed state is accepted, and the objective function has changed. For each batch of repeats, the proportion of movements are displayed. The number of movements differ with the number of accepted proposals, as a proposal might not necessary change the objective function value.

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
- use `copy_state=frigidum.annealing.naked` if `a = b` would already create a copy, or if the neighbour function return copies.

## General Advice with Simulated Annealing

- Use the movements statistics to set the starting and stopping temperature.
- Focus on the neighbour function, not the cooling scheme or acceptance variations.
- To get inspiration for random neighbours, try solve a similar problem yourself.
- Try multiple neighbours together, combinations usually work well. The `neighbours` argument expects a list of neighbours. After a run, statistics are displayed. Don't discard a neighbour just by its statistics, it might be a catalyst for a different neighbours. 
- Try add neighbours, that might work well when cold.
- Try add neighbours, that might work well when warm.
- Try add neighbours, that find a local minima with local greedy algorithm.
- Try add neighbours, that break/remove a local solution and fix it again.
- Try add neighbours, that overwrite a part of the solution rigorously. 
- It is difficult to predict the effect of a random neighbour, ideas usually don't survive the outcome of experiments.- When conditions apply, stay within the feasible zone when possible. -or-
- Only anneal on either condition or objective, not both at the same time.

## Examples

### Rastrigin Function

https://en.wikipedia.org/wiki/Rastrigin_function

```
from frigidum.examples import rastrigin

frigidum.sa(random_start=rastrigin.random_start,
           objective_function=rastrigin.rastrigin_function,
           neighbours=[rastrigin.random_small_step, rastrigin.random_big_step],
           copy_state=frigidum.annealing.naked,
           T_start=100,
           T_stop=0.00001,
           repeats=10**4)
```

## To-Do:

- Add TSP as example
- Multi threading (N simultaneous anneals)
- Drilling (after repeats, re-repeat with low temp)
- Re-Annealing.
- Re-Annealing with `N` challengers.
- Temperature dependent proposals.
- Stopping criterea for objective, i.e. stop when objective value is below certain threshold (often 0).
- (?) Auto-set start Temperature (Based on >90% movements)
- (?) Auto-stop (Based on <10% movements)
