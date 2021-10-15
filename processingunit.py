# -----
# debug
# -----

# (de)activates logging to console or file. visualizer will call itself by using python3 visual.py
LOG_CONSOLE = True
LOG_FILE = True

# activates CHECK_MEMORY. you shouldn't need to turn this on
CHECK_MEMORY = False

# check if our RAM is defined properly
def check_memory(ram, max_size):
	x = 0
	while (x < max_size):
		print('instr[', x, ']: ', ram.instr[x])
		x += 1
		
def _check_memory(ram, max_size):
	x = 0
	while x < 12:
		print('[', x, '] ', ram.data[x])
		x += 1

# ----------------
# system variables
# ----------------

# if true, runs instructions step by step (waits for input) instead of
# running everything at once
SYS_STEPS = False

# ------------------------------
# CPU architecture substructures
# ------------------------------

# ideally, we would create a python (or any language) object
# containing our CPU with every single one of these structures
# inside it, then modify them whenever needed. however, this 
# would require a major rewrite/refactor, and our calculus
# test is around the corner
# note to professor: we can rewrite this for TP2 if needed
# using the objects below as example

class cpu_CA(): # logical and arithmetic unit
	_ac = 0
	_mq = 0
	_mbr = 0
	def _lac(): # LAC: logic/arithmetic circuits
		pass

class cpu_CC(): # control unit
	_pc = 0
	_mar = 0
	_ibr = 0
	def _ctrl_circuits():
		pass # do some control signal stuff here

class cpu_prototype():
	_ca = cpu_CA()
	_cc = cpu_CC()
	def _process():
		pass # you get the idea

# MAR: memory address register (C pointer)
MAR = 0

# MQ: MUL/DIV quotient register
# used on _mul, _div (embed)
# MQ is defined in <main> (object cpu_t())

# MBR: memory buffer register
# MBR is defined in <main> (object cpu_t())

# IBR: instruction buffer register
# this is often used for pipelining: keep the first instruction
# in the register, do whatever we need to do with both instructions
# as the second one comes around.
# grimusk implements its own sort of pipeline for now, 
# so this is sort of unused, but it is simulated in processor.is_word()
IBR = 0

# IR: instruction register
# used for things like if/else, GOTO and so on
# unused in grimusk due to the fact we didn't
# reimplement control circuits from scratch... 
# ...and we don't need to
IR = 0

# PC: program counter
# defined in <main> when processing instructions

# AC: accumulation register
# defined in <main> when processing instructions

# ----------
# operations
# ----------

def _sta(instr, ram):
	MAR = instr[2] # send target address to MAR 
	ram.data[MAR] = instr[1] # sent
	if LOG_CONSOLE: print('STA called: value ', instr[1], ' saved in addr[', MAR, ']')

def _stabuf(value, addr, ram): # STA_BUFFER, same as _sta, used internally
	MAR = addr
	ram.data[MAR] = value
	if LOG_CONSOLE: print('STA called: value ', value, ' saved in addr[', MAR, ']')
	
# we ommit MAR from now onwards, you get the idea
	
def _lda(instr, ram):
	instr[1] = ram.data[instr[2]] # retrieved
	if LOG_CONSOLE: print('LDA called: value ', instr[1], ' loaded from addr[', instr[2], ']')

def _ldabuf(addr, ram): # LDA_BUFFER, ditto
	return ram.data[addr]
	if LOG_CONSOLE: print('LDA called: value ', ram.data[addr], ' loaded from addr[', addr, ']')
	
# we could also use to_sta and to_lda instead of stabuf and ldabuf, it would be slightly more realistic but
# I think it's a bit overkill. I'm keeping this here just in case, though

#def to_sta(instr, value, addr):
#	instr[2] = addr
#	instr[1] = value
#	return instr

def _sum(instr, ram):
	ram_value_a = _ldabuf(instr[1], ram)
	ram_value_b = _ldabuf(instr[2], ram)
	result = ram_value_a + ram_value_b
	_stabuf(result, instr[3], ram) # saves our variable by calling STA instead of doing so by itself
	if LOG_CONSOLE: print('SUM called: ', ram_value_a, '[', instr[1], '] + ', ram_value_b, '[', instr[2], '] = ', result, '[', instr[3], ']')

def _sumbuf(x, y, addr, ram): # SUM_BUFFER
	_stabuf((x + y), addr, ram)

def _sub(instr, ram):
	ram_value_a = _ldabuf(instr[1], ram)
	ram_value_b = _ldabuf(instr[2], ram)
	result = ram_value_a - ram_value_b
	_stabuf(result, instr[3], ram) # saves our variable by calling STA instead of doing so by itself
	if LOG_CONSOLE: print('SUB called: ', ram_value_a, '[', instr[1], '] - ', ram_value_b, '[', instr[2], '] = ', result, '[', instr[3], ']')

def _subbuf(x, y, addr, ram): # SUB_BUFFER
	_stabuf((x - y), addr, ram)
