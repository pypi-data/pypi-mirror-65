"""

Rastrigin function

https://en.wikipedia.org/wiki/Rastrigin_function

"""

import math
import random

def rastrigin_function( p ):
	"""
	 for x, y in [-5.12, 5.12]
	 global minimum at (0,0), where objective takes value 0
	"""
	x, y = p
	return (x**2 - 10 * math.cos(2 * math.pi * x)) + \
			(y**2 - 10 * math.cos(2 * math.pi * y)) + 20

def random_start():
	return ( 4 + random.random(), 4 + random.random() )

def clip( x, lower=-5.12, upper=5.12):
	return max( min(x,upper), lower)

def random_small_step(p):
	x, y = p
	return ( clip(x + 0.01 * (.5 - random.random()) ), clip(y + 0.01 * (.5 - random.random()) ))

def random_big_step(p):
	x, y = p
	return ( clip(x + 2 * (.5 - random.random()) ), clip(y + 2 * (.5 - random.random()) ))