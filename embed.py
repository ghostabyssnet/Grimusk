import grimuskbase as g
# EMBED: includes slightly more complex operations (multiply, divide...)

# ----------
# operations
# ----------

def jmp(instr):
	if g.LOG_CONSOLE: print('JMP called: PC is now ', instr[1])
	return instr[1] # 0 = opcode, 1 = where to jump

def mul(instr, ram):
	if (ram.data[instr[2]] >= 1):
		old = ram.data[instr[3]]
		ram.data[instr[2]] -= 1
		g._sumbuf(ram.data[instr[1]], ram.data[instr[3]], instr[3], ram)
		if g.LOG_CONSOLE: print('MUL called: ', old, ' + ', ram.data[instr[1]], ' = ', ram.data[instr[3]], '. (', ram.data[instr[2]], ' remaining)')
		mul(instr, ram)
	else:
		return
	# 0 = opcode; 1 = addr1; 2 = addr2; 3 = dest; 4 = counter

#def mul(instr, ram):
#	ram_value_a = ram.data[instr[1]]
#	ram_value_b = ram.data[instr[2]]
#	if (ram.data[instr[4]] <= ram.data[instr[2]]):
#		ram.data[instr[4]] += 1
#		ram.data[instr[3]] = _sum(ram_value_a, ram_value_a)
#		mul(instr, ram)
#	# 0 = opcode; 1 = addr1; 2 = addr2; 3 = dest; 4 = counter
