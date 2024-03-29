import sys
import enum
import csv
import random as rnd
import processingunit as g
import random_machine as r
import embed as e
import stdlib as std

# TODO: if we doing visualizer, watching stuff as hex would be cool

# TODO:
# [x] LDA is pipelined (c64 asm)
# [x] fix fibonnaci
# [ ] save log to file
# [x] load from file
# [x] tests
# [ ] error when trying to alloc > MAX_RAM
# [ ] ignore csv comments => do this and change from csv to .ins
# [x] implement AC
# [ ] halt throws to menu
# [x] write sample programs
# [ ] grimusk program writer
# [ ] G language
# [ ] i/o
# [ ] visualizer

# test cases
# x HLT & 0 
# x STA & 1 
# x LDA & 2 
# x SUM & 3 
# x SUB & 4 
# x MUL & 5 
# x DIV & 6 
# x AND & 7 
# x XOR & 8 
# x NOT & 9 
# ! MOV & 10 >> moved to TP2 (memory caching and multiple registers) 
# x BGR & 11
# x SMR & 12
# x JIF & 13
# x JMP & 14
# x SWP & 15
# x FIB & 16
# x POW & 17
# x SQR & 18
# x CHR & 19
# x ARR & 20
# x XLD & 21
# x XST & 22
# x XSM & 23
# x XSB & 24


# const

MAX_RAM = 1024 # 1024 "bytes", change it to whatever you want as long as it divides by 2 (binary!)

# enum & utility functions

class opcode(enum.Enum):
	# base commands
	HLT = 0 # halt
	STA = 1 # store (move to RAM)
	LDA = 2 # load (from RAM) to CPU AC
	SUM = 3 # add
	SUB = 4 # subtract
	
	# everything below is from embed (library)
	MUL = 5 # multiply
	DIV = 6 # divide
	AND = 7 # x and y (x == y)
	XOR = 8 # x or y (x != y)
	NOT = 9 # not(x)
	MOV = 10 # to be implemented with memory caches: moves data between two registers
	BGR = 11 # is bigger
	SMR = 12 # is smaller
	JIF = 13 # jump if -- basically an easier implementation of JN (jump on negative) and JZ (jump on zero)
	JMP = 14 # jump, basically GOTO
	
	# everything below is from stdlib
	SWP = 15 # uses AC to swap two values between themselves
	FIB = 16 # fibonacci
	POW = 17 # power of x
	SQR = 18 # square root (sqrt)
	# QRT = 19 # Q_sqrt or fast inverse square root
	CHR = 19 # convert to constchar (used in const vars and array heads)
	ARR = 20 # allocates array at x with size y (next y addresses are part of it)
	
	# stdlib C64 (commodore 64) assembly emulator 
	XLD = 21 # c64 lda closer to how it is in assembly
	XST = 22 # c64 sta closer to how it is in assembly
	XSM = 23 # c64 sum closer to how it is in assembly
	XSB = 24 # c64 sub closer to how it is in assembly
	# XND = [...] we'll continue c64 if there's any interest on it
	
	# everything below is from muskOS
	# stdio
	PCR = 25 # putchar()
	INP = 26 # input()
	SAV = 27 # save to disk x
	LOD = 28 # load from disk x
	AUD = 29 # play audio from addr
	
	# muskOS std
	COMPILE = 30 # compile .g program
	DISKPART = 31 # do diskpart a-la windows
	BOOT = 32 # boot muskOS
	SHUTDOWN = 33 # shutdown muskOS
	# note to professor: we want muskOS to do caching instead of grimusk itself, 
	# as unix/linux/macOS/windows generally does
	# let's ask him
	MALLOC = 34 # malloc() from addr1 to addr2 name [3] (allocates (addr1+addr2)-1 bytes)
	# addr1: [3]
	# addr1+1 to addr2: mallocd
	FREE = 35 # free() from addr1 to addr3
	IF = 36 # JIF renamed
	ELSE = 37 # notJIF
	ABORT = 38 # abort program
	TAB = 39 # change tab to x
	CALL = 40 # better JMP/JIF implementation, used in every ASM distribution
	DEF = 41 # defines variable
	SEGFAULT = 42 # segmentation fault
	AMOGUS = 43 # amogus
	AMOGAME = 44 # amogus game
	PRNSCR = 45 # print screen
	BIN = 46 # tobinary
	HEX = 47 # tohex
	STR = 48 # tostring
	BITR = 49 # bitshift to the right (>>)
	BITL = 50 # bitshift to the left (<<)
	# PANIC = 50 # kernel panic
	
	# everything below is from the console testing suite library
	# it will probably be deprecated after we implement muskOS,
	# ncurses and an actual screen
	# PRINT = 90 # print to console
	# LOG = 91 # log to file
	# ASSERT = 91 # assert value, used for testing
	# ------------------------------------------
	LEN = 24 # length of opcode, used internally
	# ------------------------------------------

# note to programmers:
# yes, I know it's ugly
# no, I won't change it for now
def to_opcode(text):
	if text == "HLT": return 0 
	elif text == "STA": return 1 
	elif text == "LDA": return 2 
	elif text == "SUM": return 3 
	elif text == "SUB": return 4 
	elif text == "MUL": return 5 
	elif text == "DIV": return 6 
	elif text == "AND": return 7 
	elif text == "XOR": return 8 
	elif text == "NOT": return 9 
	elif text == "MOV": return 10
	elif text == "BGR": return 11
	elif text == "SMR": return 12
	elif text == "JIF": return 13
	elif text == "JMP": return 14
	elif text == "SWP": return 15
	elif text == "FIB": return 16
	elif text == "POW": return 17
	elif text == "SQR": return 18
	elif text == "CHR": return 19
	elif text == "ARR": return 20
	elif text == "XLD": return 21
	elif text == "XST": return 22
	elif text == "XSM": return 23
	elif text == "XSB": return 24
	elif text == "PCR": return 25
	elif text == "INP": return 26
	else:
		print('Invalid input: ', text, '. Aborting!')
		quit()

# -------
# classes
# -------

def init_data(max_ram):
	a = []
	x = 0
	while (x < max_ram):
		a.append(0)
		x += 1
	return a

def init_instr(max_ram, opcode):
	a = []
	opcode = opcode.value
	x = 0
	while (x < max_ram):
		y = [0, 0, 0, 0, 0]
		a.append(y)
		x += 1
	x = 0
	while (x < max_ram):
		one = []
		one.append(rnd.randint(0, 4))
		for y in range(1, 4):
			one.append(rnd.randint(5, 9))
		a[x] = one
		x += 1
	return a

class instr_t(): # used as object-oriented API
	payload = [0, 0, 0, 0, 0]

class ram_t(): # ram struct
	data = [] # data memory
	instr = [] # instruction memory (array of instr_t payloads)
	def __init__(self):
		self.data = init_data(MAX_RAM)
		self.instr = init_instr(MAX_RAM, opcode.LEN)
		
class cpu_t(): # cpu struct
	pc = 0
	ac = 0
	mq = 0
	mbr = []
	
# TODO: evaluates instruction (void)
def process(instr, ram, cpu):
	# python has no switch case (?)
	op = instr[0]
	if op == opcode.HLT.value:
		if g.LOG_CONSOLE: print('HLT called: machine halted')
		return 
	
	elif op == opcode.STA.value:
		g._sta(instr, ram, cpu)
		
	elif op == opcode.LDA.value:
		g._lda(instr, ram, cpu)
	
	elif op == opcode.SUM.value:
		g._sum(instr, ram, cpu)
	
	elif op == opcode.SUB.value:
		g._sub(instr, ram, cpu)
		
	# embed library
	elif op == opcode.MUL.value:
		e._mul(instr, ram, cpu)
		
	elif op == opcode.DIV.value:
		e._div(instr, ram, cpu)
		
	elif op == opcode.AND.value:
		e._and(instr, ram, cpu)
	
	elif op == opcode.XOR.value:
		e._xor(instr, ram, cpu)
	
	elif op == opcode.BGR.value:
		e._bgr(instr, ram, cpu)
		
	elif op == opcode.SMR.value:
		e._smr(instr, ram, cpu)
	
	elif op == opcode.NOT.value:
		e._not(instr, ram, cpu)
		
	elif op == opcode.MOV.value:
		return # to be implemented w/ new registers
		
	elif op == opcode.JIF.value:
		e._jif(instr, ram, cpu)
		
	elif op == opcode.JMP.value:
		e._jmp(instr)
		
	# stdlib
	elif op == opcode.SWP.value:
		std._swp(instr, ram, cpu)
		
	elif op == opcode.FIB.value:
		std._fib(instr, ram, cpu)
		
	elif op == opcode.POW.value:
		std._pow(instr, ram, cpu)
		
	elif op == opcode.SQR.value:
		std._sqr(instr, ram, cpu)
		
	elif op == opcode.CHR.value:
		std._chr(instr, ram, cpu)
		
	elif op == opcode.ARR.value:
		std._arr(instr, ram, cpu)
		
	elif op == opcode.XLD.value:
		std._xld(instr, ram, cpu)
		
	elif op == opcode.XST.value:
		std._xst(instr, ram, cpu)
		
	elif op == opcode.XSM.value:
		std._xsm(instr, ram, cpu)
		
	elif op == opcode.XSB.value:
		std._xsb(instr, ram, cpu)

# TODO: test this 
# starts CPU and procs every command
# stored in (ram) 
def processor(ram):
	cpu = cpu_t()
	# this should be while(true) due to a machine not shutting
	# down when it doesn't have any more instructions. implement
	# it later?
	# or maybe only if we implement some kind of operating system
	while(cpu.pc < len(ram.instr)):
		# while we have instructions, our processor will
		# evaluate them
		cpu.pc += 1
		cpu.mbr = ram.instr[cpu.pc] # sends instruction to MBR
		is_word = cpu.mbr[4]
		# is_word defines if we should pipeline between this and the last instruction
		# it's considerably more complicated in a real machine, thus grimusk does it the simple way:
		# it treats the last byte as a boolean. if it's 1, then AC doesn't reset.
		# AC will always reset on simple instructions that don't require pipelining
		if is_word != 1:
			cpu.ac = 0
		if g.LOG_CONSOLE: print('Running new instruction. PC: ', cpu.pc)
		# halt if called:
		if cpu.mbr[0] == opcode.HLT.value:
			if g.LOG_CONSOLE: print('HLT called: machine stopped')
			return # halt the machine
		# 
		if cpu.mbr[0] == opcode.JMP.value:
			cpu.pc = e._jmp(ram.instr[cpu.pc]) # jumps to the defined location in memory
		process(cpu.mbr, ram, cpu)
		if g.CHECK_MEMORY == True:
			g._check_memory(ram, MAX_RAM)
		if g.SYS_STEPS == True:
			print('STEP BY STEP is activated')
			print('Press any key to continue...')
			input()

def machine_from_file():
	ram = ram_t()
	print('SETUP (1/2)')
	print('PATH TO RAM DATA FILE (../example.ram):')
	rpath = input()
	ramfile = open(rpath, 'r')
	aux = 0
	for x in ramfile:
		ram.data[aux] = (int(x))
		aux += 1
	if aux < MAX_RAM:
		while aux < MAX_RAM:
			ram.data[aux] = (rnd.randint(0, 128)) # give a random value to unused memory to properly simulate a computer
			aux += 1
	print('SETUP (2/2)')
	print('PATH TO PROGRAM/INSTRUCTION FILE (../example.csv):')
	fpath = input()
	with open(fpath) as csvfile:
		read = csv.reader(csvfile)
		line = 0
		for row in read:
			if line == 0:
				if g.LOG_CONSOLE: print('Running machine from file')
				line += 1
			else:
				if row[0].isnumeric() == False:
					row[0] = to_opcode(row[0])
					row[0] = int(row[0])
				ram.instr[line] = [int(row[0]), int(row[1]), int(row[2]), int(row[3]), int(row[4])]
				line += 1
		ram.instr[MAX_RAM - 1] = [0, 0, 0, 0, 0]
	run_machine(ram)
	
# TODO: test this
# rand machine
def random_machine():
	ram = ram_t()
	ram.data = rnd.apply_ram(MAX_RAM)
	ram.instr = rnd.apply_instr(MAX_RAM, opcode.LEN)
	# montarRam() done
	run_machine(ram)

def boot():
	if MAX_RAM: # check if something went wrong with our const
		if g.LOG_CONSOLE: print('MEMORY OK')
		if g.LOG_CONSOLE: print('STARTING CPU')
	else: quit()

# runs the machine
# ram = ram payload (as in the class/struct)
# call this only from random_machine or machine_from_file
# (or any new stuff), never from python itself
def run_machine(ram):
	boot()
	processor(ram)
	
def main():
	print('---------- bcc266 ----------')
	print('grimusk: computer simulation')
	print('----------------------------')
	print('')
	print('MENU:')
	print('- PRESS 1 TO LOAD MACHINE FROM FILE')
	print('- PRESS ANY OTHER KEY TO USE RANDOM VALUES')
	x = input()
	if (x == '1'):
		machine_from_file()
	else:
		random_machine()


main()
