import processingunit as g
import embed as e

# ----------
# operations
# ----------

# grimusk pretty much writes programs by itself by now
# our functions soft-pipeline themselves

# SWP: swap values between themselves using AC
def _swp(instr, ram, cpu):
	g._lda(instr, ram, cpu) # loads instr[1] to AC
	g._stabuf(ram.data[instr[2]], instr[1], ram) # sets data at [1] to data from [2]
	g._stabuf(cpu.ac, instr[2], ram) # sets data at [2] to data from AC

# FIB: fibonacci instr[1] to instr[2]
def _fib(instr, ram):
	e._and()














# -------
# c64 asm
# -------

def _xld(instr, ram, cpu):
	cpu.ac = ram.data[instr[1]]
	# 0 = payload; 1 = addr

def _xldbuf(addr, ram, cpu):
	cpu.ac = ram.data[addr]
	
def _xst(instr, ram, cpu):
	ram.data[instr[1]] = cpu.ac
	# 0 = payload; 1 = addr

# xsm does not have a third instruction. it expects a STA to come afterwards
# if it doesn't, nothing happens, just like in old asm (c64, neander, ahmes)
# more info at https://www.youtube.com/watch?v=9hLGvLvTs1w
# our next instructions will follow this principle... regularly
# formula: (ac = LDA addr1) + val addr2 -> ac
# material em portugues: https://www.lnaffah.com/oc2013-1/material/Organizacao_Processador_Neander.pdf
def _xsm(instr, ram, cpu):
	cpu.ac = _xldbuf(instr[1])
	# as you can see, we'll also rely less on python and more on our own functions
	ram_b = ram.data[instr[2]]
	cpu.ac += ram_b # '+' can be treated as a half-adder or a full-adder
	# ac is now loaded with (a + b). STA should store it wherever our instr[3] would be
	# 0 = payload; 1 = addr1; 2 = addr2;

def _xsb(instr, ram, cpu):
	cpu.ac = _xldbuf(instr[1])
	ram_b = ram.data[instr[2]]
	cpu.ac -= ram_b
	# 0 = payload; 1 = addr1; 2 = addr2;

def _xnd(instr, ram):
	# closer to old C64 assembly: if x - y = 0, they're equal
	# yes, x - (-y) will be x + y, however, negative numbers in binary
	# are set by having 1 as their first term ((10000001) = -(00000001))
	# and there are other checks to ensure things go as planned
	pass
