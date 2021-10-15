import processingunit as g
# ----------
# operations
# ----------

# grimusk pretty much writes programs by itself by now

def _xsm(instr, ram, cpu):
	

def _xnd(instr, ram):
	# closer to old C64 assembly: if x - y = 0, they're equal
	# yes, x - (-y) will be x + y, however, negative numbers in binary
	# are set by having 1 as their first term ((10000001) = -(00000001))
	# and there are other checks to ensure things go as planned
	g._subbuf()
	
def _bol(instr, ram):
