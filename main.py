import sys
import enum
import csv
import random as rnd
import grimuskbase as g
import random_machine as r
import embed
import stdlib as std

# TODO: if we doing visualizer, watching stuff as hex would be cool

# TODO:
# opcodes
# 	[x] 5
# 	[ ] 6
# 	[ ] 7
# 	[ ] 8
# 	[ ] 9
# 	[ ] 10
# 	[ ] 11
# 	[ ] 12
# 	[ ] 13
# 	[ ] 14
# 	[ ] 15
# 	[ ] 16
# [ ] save log to file
# [ ] load from file
# [ ] tests
# [ ] implement AC
# visualizer

# const

MAX_RAM = 1024 # 1024b, change it to whatever you want as long as it divides by 2 (binary!)

# enum & utility functions

class opcode(enum.Enum):
	HLT = 0 # halt
	STA = 1 # store (move to RAM)
	LDA = 2 # load (from RAM)
	SUM = 3 # add
	SUB = 4 # subtract
	
	# everything below is from embed (library)
	MUL = 5 # multiply
	DIV = 6 # divide
	XOR = 7 # x or y
	AND = 8 # x and y
	NOT = 9 # not(x)
	MOV = 10 # to be implemented with mem. caches: moves data between two registers
	JMP = 11 # jump, basically GOTO
	
	# everything below is from stdlib
	CHR = 12 # putchar()
	FIB = 13 # fibonacci
	POW = 14 # power of x
	SQR = 15 # square root (sqrt)
	QRT = 16 # Q_sqrt or fast inverse square root
	
	# ------------------------------------------
	LEN = 16 # length of opcode, used internally
	# ------------------------------------------

def to_opcode(text):
	if text == "HLT": return 0 
	elif text == "STA": return 1 
	elif text == "LDA": return 2 
	elif text == "SUM": return 3 
	elif text == "SUB": return 4 
	elif text == "MUL": return 5 
	elif text == "DIV": return 6 
	elif text == "XOR": return 7 
	elif text == "AND": return 8 
	elif text == "NOT": return 9 
	elif text == "MOV": return 10
	elif text == "JMP": return 11
	elif text == "FIB": return 12
	elif text == "POW": return 13
	elif text == "SQR": return 14
	elif text == "QRT": return 15
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

class ram_t():
	data = [] # data memory
	instr = [] # instruction memory (array of instr_t payloads)
	def __init__(self):
		self.data = init_data(MAX_RAM)
		self.instr = init_instr(MAX_RAM, opcode.LEN)

# TODO: evaluates instruction (void)
def process(instr, ram, ac):
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
		embed.mul(instr, ram)

# TODO: test this 
# starts CPU and procs every command
# stored in (ram) 
def cpu(ram):
	pc = 0
	ac = 0
	# this should be while(true) due to a machine not shutting
	# down when it doesn't have any more instructions. implement
	# it later?
	while(pc < len(ram.instr)):
		# while we have instructions, our processor will
		# evaluate them
		ac = 0
		pc += 1
		aux = ram.instr[pc]
		if g.LOG_CONSOLE: print('Running new instruction. PC: ', pc)
		if aux[0] == opcode.HLT.value:
			if g.LOG_CONSOLE: print('HLT called: machine stopped')
			return # halt the machine
		if aux[0] == opcode.JMP.value:
			pc = embed.jmp(ram.instr[pc]) # jumps to the defined location in memory
		#g._check_memory(ram, MAX_RAM)
		process(ram.instr[pc], ram, ac)
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

# TODO: test properly
# runs the machine
# ram = ram payload (as in the class/struct)
# call this only from random_machine or machine_from_file
# (or any new stuff), never from python itself
def run_machine(ram):
	boot()
	cpu(ram)
	
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
