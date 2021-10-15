import processingunit as g

# EMBED: includes slightly more complex operations (multiply, divide...)

# ----------
# operations
# ----------

# we abstract from MBR, PC and stuff from now on
# or else it will take decades to code properly

def _jmp(instr):
	if g.LOG_CONSOLE: print('JMP called: PC is now ', instr[1])
	return instr[1] # 0 = opcode, 1 = where to jump

def _mul(instr, ram, cpu):
	if cpu.mq == 0:
		if ram.data[instr[1]] == 0 or ram.data[instr[2]] == 0:
			g._stabuf(0, instr[3], ram)
			return
		if ram.data[instr[1]] == 1:
			g._stabuf(ram.data[instr[2]], instr[3], ram)
			return
		if ram.data[instr[2]] == 1:
			g._stabuf(ram.data[instr[1]], instr[3], ram)
			return
	if (ram.data[instr[2]] <= cpu.mq):
		cpu.mq += 1
		old = ram.data[instr[3]]
		g._sumbuf(ram.data[instr[1]], ram.data[instr[3]], instr[3], ram)
		if g.LOG_CONSOLE: print('MUL called: ', old, ' + ', ram.data[instr[1]], ' = ', ram.data[instr[3]], '. (', ram.data[instr[2]], ' remaining)')
		_mul(instr, ram, cpu)
	else:
		cpu.mq = 0
		return
	
def _div(instr, ram, cpu): # TODO: carry-over
	if cpu.mq == 0:
		ram.data[instr[3]] = ram.data[instr[1]]
		if ram.data[instr[1]] == 0 or ram.data[instr[2]] == 0:
			return
		if ram.data[instr[1]] == 1:
			g._stabuf(ram.data[instr[2]], instr[3], ram)
			return
		if ram.data[instr[2]] == 1:
			g._stabuf(ram.data[instr[1]], instr[3], ram)
			return
	if (ram.data[instr[3]] >= ram.data[instr[2]]):
		cpu.mq += 1
		g._subbuf(ram.data[instr[3]], ram.data[instr[2]], instr[3], ram) # reduces 1 by 2 then saves in addr1
		g._stabuf(ram.data[instr[1]], instr[3], ram) # also saves in addr3 (target address)
		if g.LOG_CONSOLE: print('DIV called: ', old, ' - ', ram.data[instr[2]], ' = ', ram.data[instr[3]], '. (should be equal to ', ram.data[instr[1]], ')')
		_div(instr, ram, cpu)
	else:
		cpu.mq = 0
		return

def _and(instr, ram):
	if (ram.data[instr[1]] == ram.data[instr[2]]): g._stabuf(1, instr[3], ram)
	# 0 = opcode; 1 = addr1; 2 = addr2; 3 = dest;
	
def _xor(instr, ram):
	if (ram.data[instr[1]] != ram.data[instr[2]]): g._stabuf(1, instr[3], ram)
	# 0 = opcode; 1 = addr1; 2 = addr2; 3 = dest;

def _not(instr, ram):
	ram.data[instr[2]] = -(int(ram.data[instr[1]]))
	# 0 = opcode; 1 = addr1; 2 = dest;
	
def _mov(instr, ram):
	pass # TODO: when we have cache

def _bgr(instr, ram):
	if (ram.data[instr[1]] > ram.data[instr[2]]): g._stabuf(1, instr[3], ram)
	# 0 = opcode; 1 = addr1; 2 = addr2; 3 = dest;
	
def _smr(instr, ram):
	if (ram.data[instr[1]] < ram.data[instr[2]]): g._stabuf(1, instr[3], ram)
	# 0 = opcode; 1 = addr1; 2 = addr2; 3 = dest;
	
def _jif(instr, ram, cpu):
	if (ram.data[instr[1]] == 1): cpu.pc = ram.data[instr[2]]
	# 0 = opcode; 1 = is_true; 2 = addr
