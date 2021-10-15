import random
import grimuskbase as g

# applies random values to a grimusk machine's ram
def apply_ram(ram_size):
	x = 0
	ret = []
	while (x < ram_size):
		ret.append(random.randint(0, 128)) 
		x += 1
	return ret

# args: RAM_SIZE && length of opcode enum 
def apply_instr(ram_size, i_size):
	x = 0
	i_size = i_size.value
	ret = []
	z = 0
	while (z < ram_size):
		ret.append(0)
		z += 1
	while (x < ram_size):
		one = []
		one.append(random.randint(0, i_size))
		for y in range(1, 4):
			one.append(random.randint(0, 16))
		ret[x] = one 
		x += 1
	return ret
