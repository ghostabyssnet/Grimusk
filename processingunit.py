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

def _sta(instr, ram, cpu):
	MAR = instr[1] # send target address to MAR 
	ram.data[MAR] = cpu.ac # sent
	if LOG_CONSOLE: print('STA called: value ', cpu.ac, ' saved in addr[', MAR, ']')

def _stabuf(value, addr, ram): # STA_BUFFER, same as _sta, used internally
	MAR = addr
	ram.data[MAR] = value
	if LOG_CONSOLE: print('STA called: value ', value, ' saved in addr[', MAR, ']')
	
# we ommit MAR from now onwards, you get the idea
	
def _lda(instr, ram, cpu):
	cpu.ac = ram.data[instr[1]] # retrieved
	if LOG_CONSOLE: print('LDA called: value ', cpu.ac, ' loaded from addr[', instr[1], ']')

def _ldabuf(addr, ram): # LDA_BUFFER, ditto
	return ram.data[addr]
	if LOG_CONSOLE: print('LDA called: value ', ram.data[addr], ' loaded from addr[', addr, ']')

def _lda_ac(value, cpu): # LDA_BUFFER but to AC
	cpu.ac = value
	if LOG_CONSOLE: print('LDA called: value ', value, ' stored into AC (', cpu.ac, ')')

# we could also use to_sta and to_lda instead of stabuf and ldabuf, it would be slightly more realistic but
# I think it's a bit overkill. I'm keeping this here just in case, though

#def to_sta(instr, value, addr):
#	instr[2] = addr
#	instr[1] = value
#	return instr

def _sum(instr, ram, cpu): # SUM between two numbers
	_lda_ac(ram.data[instr[1]], cpu) # sends instr[1] to AC
	_lda_ac((cpu.ac + ram.data[instr[2]]), cpu) # adds instr[2] and stores in AC
	if LOG_CONSOLE: print('SUM called: ', ram.data[instr[1]], '[', instr[1], '] + ', ram.data[instr[2]], '[', instr[2], '] = ', cpu.ac, '.')

def _sumbuf(x, y, addr, ram): # SUM_BUFFER
	if LOG_CONSOLE: print('SUM called: ', x, ' + ', y, ' = ', (x + y), '.')
	_stabuf((x + y), addr, ram)

def _sum_ac(value, value2, cpu): # SUM_BUFFER to AC
	if LOG_CONSOLE: print('SUM called: ', value, ' + ', value2, ' = ', (value + value2), ' (AC)')
	_lda_ac((value + value2), cpu)

def __sum(instr, ram): # SUM as it's done by our professor. deprecated because it's not really keen to pipelining
	# we did try, though. see below for a half-half solution that uses _stabuf to store stuff
	ram_value_a = _ldabuf(instr[1], ram)
	ram_value_b = _ldabuf(instr[2], ram)
	result = ram_value_a + ram_value_b
	_stabuf(result, instr[3], ram) # saves our variable by calling STA instead of doing so by itself
	if LOG_CONSOLE: print('SUM called: ', ram_value_a, '[', instr[1], '] + ', ram_value_b, '[', instr[2], '] = ', result, '[', instr[3], ']')

def _sub(instr, ram, cpu):
	_lda_ac(ram.data[instr[1]], cpu) # sends instr[1] to AC
	_lda_ac((cpu.ac - ram.data[instr[2]]), cpu) # adds instr[2] and stores in AC
	if LOG_CONSOLE: print('SUB called: ', ram.data[instr[1]], '[', instr[1], '] - ', ram.data[instr[2]], '[', instr[2], '] = ', cpu.ac, '.')

def __sub(instr, ram): # same issue as SUM. deprecated, but usable anyway
	ram_value_a = _ldabuf(instr[1], ram)
	ram_value_b = _ldabuf(instr[2], ram)
	result = ram_value_a - ram_value_b
	_stabuf(result, instr[3], ram) # saves our variable by calling STA instead of doing so by itself
	if LOG_CONSOLE: print('SUB called: ', ram_value_a, '[', instr[1], '] - ', ram_value_b, '[', instr[2], '] = ', result, '[', instr[3], ']')

def _subbuf(x, y, addr, ram): # SUB_BUFFER
	if LOG_CONSOLE: print('SUM called: ', x, ' - ', y, ' = ', (x - y), '[', addr, ']')
	_stabuf((x - y), addr, ram)
