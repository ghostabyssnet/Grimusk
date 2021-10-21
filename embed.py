import processingunit as g

# EMBED: includes slightly more complex operations (multiply, divide...)

# ----------
# operations
# ----------

# we abstract from MBR, PC and stuff from now on
# or else it will take a while to code properly

# JMP to target PC
def _jmp(instr):
	if g.LOG_CONSOLE: print('JMP called: PC is now ', instr[1])
	return instr[1] # 0 = opcode, 1 = where to jump

def _jmp_ac(cpu): # JMP using AC value, more realistic
	if g.LOG_CONSOLE: print('JMP called: PC is now ', cpu.ac)
	cpu.pc = cpu.ac

# MUL and DIV use the CPU's MQ (mul/div quotient register)

# MULtiply
def _mul(instr, ram, cpu):
	if cpu.mq == 0:
		cpu.mq += 1
		g._lda_ac(ram.data[instr[1]], cpu) # sets AC to 0
		if ram.data[instr[1]] == 0 or ram.data[instr[2]] == 0:
			g._lda_ac(0, cpu)
			return
		if ram.data[instr[1]] == 1:
			g._lda_ac(ram.data[instr[2]], cpu)
			return
		if ram.data[instr[2]] == 1:
			g._lda_ac(ram.data[instr[1]], cpu)
			return
	cpu.mq += 1
	if (cpu.mq <= ram.data[instr[2]]):
		old = cpu.ac
		g._lda_ac(cpu.ac + ram.data[instr[1]], cpu) # adds AC and addr2, stores in AC
		if g.LOG_CONSOLE: print('MUL called: ', old, ' + ', ram.data[instr[1]], ' = ', cpu.ac, '. (', cpu.mq, '/', ram.data[instr[2]], ' done)')
		_mul(instr, ram, cpu)
	else:
		cpu.mq = 0
		return

# DIVide
# opcode, addr1, addr2, unused, 1
def _div(instr, ram, cpu):
	if cpu.mq == 0:
		g._lda_ac(ram.data[instr[1]], cpu) # sends instr[1] value to AC
		if ram.data[instr[1]] == 0 or ram.data[instr[2]] == 0:
			return
		if ram.data[instr[1]] == 1:
			g._lda_ac(ram.data[instr[2]], cpu)
			return
		if ram.data[instr[2]] == 1:
			g._lda_ac(ram.data[instr[1]], cpu)
			return
	cpu.mq += 1
	if (cpu.ac >= ram.data[instr[2]]):
		old = cpu.ac
		g._lda_ac(cpu.ac - ram.data[instr[2]], cpu) # reduces AC by addr2, stores in AC
		if g.LOG_CONSOLE: print('DIV called: ', old, ' - ', ram.data[instr[2]], ' = ', cpu.ac, '.', cpu.mq)
		_div(instr, ram, cpu)
	else:
		cpu.ac = cpu.mq - 1 # final number is times ran - 1
		if g.LOG_CONSOLE: print('DIV result: ', cpu.ac, '.')
		cpu.mq = 0
		return

# AND: is equal
def _and(instr, ram, cpu):
	if g.LOG_CONSOLE: print('AND called: checking if ', ram.data[instr[1]], ' is equal to ', ram.data[instr[2]], '.')
	if (ram.data[instr[1]] == ram.data[instr[2]]): g._lda_ac(1, cpu) # stores 1 (true) to AC
	# an implementation without == would be (x + y == 0) or something similar
	# as seen in C64
	# 0 = opcode; 1 = value;

# XOR: is not equal
def _xor(instr, ram, cpu):
	if g.LOG_CONSOLE: print('OR called: checking if ', ram.data[instr[1]], ' is not equal to ', ram.data[instr[2]], '.')
	if (ram.data[instr[1]] != ram.data[instr[2]]): g._lda_ac(1, cpu) # stores 1 (true) to AC
	# 0 = opcode; 1 = value;

# NOT: reverse/negative of
def _not(instr, ram, cpu):
	if g.LOG_CONSOLE: print('NOT called: reversing ', ram.data[instr[1]], '.')
	g._lda_ac((int(ram.data[instr[1]])), cpu) # loads to AC
	g._stabuf((- cpu.ac), instr[2], ram) # stores inverse to dest
	# 0 = opcode; 1 = addr1; 2 = dest;

# MOV: move between registers
def _mov(instr, ram, cpu):
	pass # TODO: when we have cache

# BGR: is bigger than
def _bgr(instr, ram, cpu):
	if g.LOG_CONSOLE: print('BGR called: checking if ', ram.data[instr[1]], ' is bigger than ', ram.data[instr[2]], '.')
	if (ram.data[instr[1]] > ram.data[instr[2]]): g._lda_ac(1, cpu)
	# 0 = opcode; 1 = addr1; 2 = addr2;

# SMR: is smaller than
def _smr(instr, ram, cpu):
	if g.LOG_CONSOLE: print('SMR called: checking if ', ram.data[instr[1]], ' is smaller than ', ram.data[instr[2]], '.')
	if (ram.data[instr[1]] < ram.data[instr[2]]): g._lda_ac(1, cpu)
	# 0 = opcode; 1 = addr1; 2 = addr2;

# JIF: will jump if AC = 1 (true)
# this instruction is pipelined (is_word == 1)
def _jif(instr, ram, cpu):
	if g.LOG_CONSOLE: print('JIF called: jumping if AC is 1 (AC = ', cpu.ac, ')')
	if (cpu.ac == 1): 
		g._lda(instr, ram, cpu)
		_jmp_ac(cpu)
	# 0 = opcode; 1 = addr to jmp
