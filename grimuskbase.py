# (de)activates logging to console or file. visualizer will call itself by using python3 visual.py
LOG_CONSOLE = True
LOG_FILE = True

# ----------
# operations
# ----------

def _sta(instr, ram):
	ram.data[instr[2]] = instr[1] # sent
	if LOG_CONSOLE: print('STA called: value ', instr[1], ' saved in addr[', instr[2], ']')

def _stabuf(value, addr, ram): # STA_BUFFER, same as _sta, used internally
	ram.data[addr] = value
	if LOG_CONSOLE: print('STA called: value ', value, ' saved in addr[', addr, ']')
	
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
	
# -----
# debug
# -----

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
