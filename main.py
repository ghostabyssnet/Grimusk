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
# opcodes
# 	[x] 5
# 	 	[ ] mul(0), mul(1)
# 	[x] 6
# 	 	[ ] div(0), div(1)
# 	[ ] 7 AND
# 	[ ] 8 XOR 
# 	[ ] 9 NOT
# 	[ ] 10 MOV
# 	[ ] 11 BGR 
# 	[ ] 12 SMR
# 	[ ] 13 JMP
# 	[ ] 14
# 	[ ] 15
# 	[ ] 16
# [ ] NOT is pipelined
# [ ] LDA is pipelined
# [ ] save log to file
# [x] load from file
# [x] tests
# [ ] implement AC
# [ ] halt throws to menu
# [ ] program writer
# [ ] G language
# [ ] i/o
# [ ] visualizer

# const

MAX_RAM = 1024 # 1024b, change it to whatever you want as long as it divides by 2 (binary!)

# enum & utility functions

class opcode(enum.Enum):
	# base commands
	HLT = 0 # halt
	STA = 1 # store (move to RAM)
	LDA = 2 # load (from RAM)
	SUM = 3 # add
	SUB = 4 # subtract
	
	# everything below is from embed (library)
	MUL = 5 # multiply
	DIV = 6 # divide
	AND = 7 # x and y (x == y)
	XOR = 8 # x or y (x != y)
	NOT = 9 # not(x)
	MOV = 10 # to be implemented with mem. caches: moves data between two registers
	BGR = 11 # is bigger
	SMR = 12 # is smaller
	JMP = 13 # jump, basically GOTO
	
	# everything below is from stdlib
	CHR = 14 # putchar()
	FIB = 15 # fibonacci
	POW = 16 # power of x
	SQR = 17 # square root (sqrt)
	QRT = 18 # Q_sqrt or fast inverse square root
	XSM = 19 # c64 sum: sum closer to how it is in assembly
	XSB = 20 # c64 sub: sub closer to how it is in assembly
	XND = 21 # c64 and: written closer to assembly
	
	# ------------------------------------------
	LEN = 21 # length of opcode, used internally
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
	elif text == "JMP": return 13
	elif text == "CHR": return 14
	elif text == "FIB": return 15
	elif text == "POW": return 16
	elif text == "SQR": return 17
	elif text == "QRT": return 18
	elif text == "XSM": return 19
	elif text == "XSB": return 20
	elif text == "XND": return 21
	else:
		print('Invalid input file!')
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
	mbr = []
	
# TODO: evaluates instruction (void)
def process(instr, ram, cpu):
	# python has no switch case (?)
	op = instr[0]
	if op == opcode.HLT.value:
		if g.LOG_CONSOLE: print('HLT called: machine halted')
		return 
	
	elif op == opcode.STA.value:
		g._sta(instr, ram)
		
	elif op == opcode.LDA.value:
		g._lda(instr, ram)
	
	elif op == opcode.SUM.value:
		g._sum(instr, ram)
	
	elif op == opcode.SUB.value:
		g._sub(instr, ram)
		
	# embed library
	elif op == opcode.MUL.value:
		e._mul(instr, ram)

# TODO: test this 
# starts CPU and procs every command
# stored in (ram) 
def processor(ram):
	cpu = cpu_t()
	pc = cpu.pc
	ac = cpu.ac
	mbr = cpu.mbr
	# this should be while(true) due to a machine not shutting
	# down when it doesn't have any more instructions. implement
	# it later?
	# or maybe only if we implement some kind of operating system
	while(pc < len(ram.instr)):
		# while we have instructions, our processor will
		# evaluate them
		pc += 1
		mbr = ram.instr[pc]
		is_word = mbr[4]
		# is_word defines if we should pipeline between this and the last instruction
		# it's considerably more complicated in a real machine, thus grimusk does it the simple way:
		# it treats the last byte as a boolean. if it's 1, then AC doesn't reset.
		# AC will always reset on simple instructions that don't require pipelining
		if is_word != 1:
			ac = 0
		if g.LOG_CONSOLE: print('Running new instruction. PC: ', pc)
		# halt if called:
		if mbr[0] == opcode.HLT.value:
			if g.LOG_CONSOLE: print('HLT called: machine stopped')
			return # halt the machine
		# 
		if mbr[0] == opcode.JMP.value:
			pc = e._jmp(ram.instr[pc]) # jumps to the defined location in memory
		process(mbr, ram, ac)
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
	ram.data = r.apply_ram(MAX_RAM)
	ram.instr = r.apply_instr(MAX_RAM, opcode.LEN)
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
		pass
		# random_machine()


main()
