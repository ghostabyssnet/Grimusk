import processingunit as g
import embed as e

# ----------
# operations
# ----------

# grimusk pretty much writes programs by itself by now
# our functions soft-pipeline themselves

# SWP: swap values between themselves using AC
# opcode, value1, value2, unused, 0
def _swp(instr, ram, cpu):
	g._lda(instr, ram, cpu) # loads instr[1] to AC
	g._stabuf(ram.data[instr[2]], instr[1], ram) # sets data at [1] to data from [2]
	g._stabuf(cpu.ac, instr[2], ram) # sets data at [2] to data from AC

# FIB: fibonacci until instr[1] to AC
# opcode, limit, alloc_start, unused, 1 (is_word())
# fib allocates 3 bytes (allocstart + 2) as variables
# neg fib should be defined as NOT (fib). they're mirrored
# make sure alloc_start is 0 before (use STA)
def _fib(instr, ram, cpu):
	if (ram.data[instr[1]] == 0 or ram.data[instr[1]] == 1):
		g._lda_ac(ram.data[instr[1]], cpu)
		return
	if ram.data[instr[1]] == -1:
		g._lda_ac(1, cpu)
		return
	if ram.data[instr[2]] == 0:
		g._stabuf(2, instr[2], ram) # make sure we start at 2
		g._stabuf(1, (instr[2] + 1), ram) # allocate another byte
		g._stabuf(0, (instr[2] + 2), ram) # allocate another byte
		# we could use MQ for this but to be honest idk if that would be legitimate
	if ram.data[instr[2]] <= ram.data[instr[1]]: # count until limit
		g._lda_ac((ram.data[instr[2+2]] + ram.data[instr[2+1]]), cpu)
		g._ram.data[instr[2+2]] = ram.data[instr[2+1]]
		g._stabuf(cpu.ac, (instr[2] + 1), ram)
		g._stabuf((ram.data[instr[2]] + 1), ram.data[instr[2]], ram) 
		_fib(instr, ram, cpu)

# POWer of
# opcode, value, times, unused, 1
def _pow(instr, ram, cpu):
	if ram.data[instr[2]] == 0:
		g._lda_ac(1, cpu)
		return
	if ram.data[instr[2]] == 1:
		g._lda_ac(ram.data[instr[1]], cpu)
		return
	if cpu.mq == 0:
		cpu.ac = ram.data[instr[1]]
	cpu.mq += 1
	if cpu.mq <= ram.data[instr[2]]:
		_sum_ac(cpu.ac, ram.data[instr[1]], cpu)
		_pow(instr, ram, cpu)
	else:
		cpu.mq = 0

# SQR (sqrt) square root of
# opcode, value, alloc_start, unused, 1
# allocates 3 bytes (allocstart + 2)
# using the CORDIC method:
# https://www.convict.lu/Jeunes/Math/square_root_CORDIC.htm
def _sqr(instr, ram, cpu):
	if cpu.mq = 0:
		g._stabuf(128, (instr[2] + 1), ram)
		g._stabuf(0, (instr[2] + 2), ram)
	cpu.mq += 1
	if cpu.mq <= 8:
		g._stabuf(ram.data[instr[2] + 1], (instr[2] + 2), ram)
		if ((ram.data[instr[2] + 2] * ram.data[instr[2] + 2]) > ram.data[instr[1]]):
			# we could also use _pow() to do this, but it would require some payload
			# conversion that would be annoying to do, as _pow() takes a different set of instr 
			g._stabuf((ram.data[instr[2] + 2] - ram.data[instr[2] + 1]), (instr[2] + 1), ram)
		g._stabuf((ram.data[instr[2] + 1] / 2), (instr[2] + 1), ram) # same issue as above
		# we could also use _div() but it would take some annoyance to do
		g._lda_ac(ram.data[instr[2] + 2]) # store in AC
	else:
		cpu.mq = 0


# convert to const char
# used to define constant system variables like array heads
# opcode, targetaddr, 0, 0, 0
def _chr(instr, ram, cpu):
	g._stabuf("__const", instr[1], ram) # saves __const into addr[1]
	# we could convert this to binary or int and add flags to make it more realistic but why bother

# defines a new array
# uses n + 2 bytes as addresses (yes, this is not as optimized as computers nowadays)
# [__const, SIZEOF, n0, n1, n2... n]
# of course we have malloc to use this properly later on, as the C language did (eventually)
# opcode, start_addr, size, 0, 1
def _arr(instr, ram, cpu):
	if cpu.mq = 0: # using cpu.mq because we don't have access to other registers yet (TP2?)
		_chr(instr, ram, cpu) # store __const to start_addr (addr[0])
		g._stabuf(ram.data[instr[2]], (instr[1] + 1), ram) # sets addr[1] as SIZEOF 
		g._lda_ac(instr[1] + 2) # set AC to address[n + 2], after __const and SIZEOF
	cpu.mq += 1
	if cpu.mq <= ram.data[instr[2]]:
		g._stabuf(0, cpu.ac, ram) # store 0 into addr[AC]
		g._sum_ac(ac, 1, cpu) # adds 1 to AC
		_arr(instr, ram, cpu) # calls itself recursively until it fills the array
	else:
		cpu.mq = 0

# note to professor:
# there's absolutely no way to do this fully in assembly until
# the time to give you the assignment, sorry
# -----------------
# implementation of the infamous Q_sqrt (Q_rsqrt or fast inverse square root)
# this algorithm alone made 3D games possible after Quake 3
# https://en.wikipedia.org/wiki/Fast_inverse_square_root
def _qrt(instr, ram, cpu):
	g._lda_ac(1597463007, cpu) # magic number constant 0x5F3759DF
	g._lda_ac((cpu.ac - (cpu.ac / 2)), cpu) # what the fuck?
	g._lda_ac((cpu.ac * 1.5 - ((ram.data[instr[1]] * 0.5) * cpu.ac * cpu.ac)))

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
