import numpy as np
import random

def test():
	x = 0
	_max = 8
	a = np.array([], [])
	print('start: ', a)
	while (x < _max):
		one = []
		one.append(random.randint(0, 4))
		for y in range(1, 4):
			one.append(random.randint(5, 9))
		a = np.append([x], one, axis=0)
		print(x, ': ', a)
		x += 1

def _test():
	x = 0
	_max = 8
	arr = []
	z = 0
	while (z < _max):
		arr.append(127)
		z += 1
	while (x < _max):
		one = []
		one.append(random.randint(0, 4))
		for y in range(1, 4):
			one.append(random.randint(5, 9))
		arr[x] = one
		x += 1
		# ...
	x = 0
	while (x < len(arr)):
		print(arr[x])
		x += 1
	print('')
	print(arr)
_test()		
#test()
