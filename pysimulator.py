# create cpu state

registers = [0] * 32
pc = 0
mem = bytearray(4096)
# each byte will be 2 Hex's or 4 bits each

#this will get the opcode since it is the lower 7 bits for RISCV
#masking
def get_opcode(instruction):
    return instruction & 0x7F

# we can use shift right to compare the bits we need

def get_rd(instruction):
    return (instruction >> 7) & 0x1F

def get_func3(instruction):
    return (instruction >> 12) & 0x07

def get_rs1(instruction):
    return (instruction >> 15) & 0x1F

def get_rs2(instruction):
    return (instruction >> 20) & 0x1F

def get_func7(instruction):
    return (instruction >> 25) & 0x7F


instr = 0x00500113

print(hex(get_opcode(instr)))  # should be 0x13
print(hex(get_rd(instr)))      # should be 0x2  (register x2)
print(hex(get_func3(instr)))   # should be 0x0
print(hex(get_rs1(instr)))     # should be 0x0  (register x0)
print(hex(get_rs2(instr)))     # should be 0x5
print(hex(get_func7(instr)))   # should be 0x0