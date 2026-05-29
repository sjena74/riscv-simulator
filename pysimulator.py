# building a riscv simulator in python for rv32I 
# using 32 registers and pc 


registers = [0] * 32
pc = 0
running = True
mem = bytearray(4096)
# each byte will be 2 hexes or 4 bits each

# for signed instructions
def s32(x):
    x = x & 0xFFFFFFFF
    if (x & 0x80000000):
        return x - 0x100000000
    return x
    
# use to write back to register
def u32(x):
    return x & 0xFFFFFFFF

# this will get the opcode since it is the lower 7 bits for RISCV
# masking
def get_opcode(instruction):
    return instruction & 0x7F

# we can use shift right to compare the bits we need
# for R-Type and will be reused for other types
# little-endian for riscv
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

# For I-Type
def get_imm(instruction):

    imm = (instruction >> 20) & 0xFFF
    if (imm & 0x800):
        imm -= 0x1000
    return imm


# For S-Type (sign bit is 11)
def get_imm_s(instruction):
    imm_7 = (instruction >> 25) & 0x7F
    imm_5 = (instruction >> 7) & 0x1F
    imm = (imm_7 << 5) | imm_5
    if (imm & 0x800):
        imm = imm - 0x1000
    return imm

# For B-Type (sign bit is 12, bit 0 is 0) 
def get_imm_b(instruction):
    imm_4b = (instruction >> 8) & 0xF
    imm_6b = (instruction >> 25) & 0x3F
    imm_11 = (instruction >> 7) & 0x1
    imm_12 = (instruction >> 31) & 0x1
    imm = (imm_12 << 12) | (imm_11 << 11) | (imm_6b << 5) | (imm_4b << 1)
    if (imm & 0x1000):
        imm = imm - 0x2000
    return imm

# For J-Type (20 bits, bit 0 is 0)
def get_imm_j(instruction):
    imm_20 = (instruction >> 31) & 0x1
    imm_10_1 = (instruction >> 21) & 0x3FF
    imm_11 = (instruction >> 20) & 0x1
    imm_19_12 = (instruction >> 12) & 0xFF

    imm = (imm_20 << 20) | (imm_19_12 << 12) | (imm_11 << 11) | (imm_10_1 << 1)
    if (imm & 0x100000):
        imm = imm - 0x200000
    return imm

# For U-Type (20 bits)
def get_imm_u(instruction):
    imm = instruction & 0xFFFFF000
    return imm

## Basic CPU simulator logic

# Load Word
def load_word(address):
    if (address < 0 or address + 3 >= len(mem)):
        raise Exception("Memory read is out of bounds.")
    return (mem[address] | mem[address + 1] << 8 | mem[address + 2] << 16 | mem[address + 3] << 24)

# Store Word
def store_word(address, val):
    if (address < 0 or address + 3 >= len(mem)):
        raise Exception("Memory write out of bounds.")
    val = u32(val)
    mem[address] = val & 0xFF
    mem[address + 1] = (val >> 8) & 0xFF
    mem[address + 2] = (val >> 16) & 0xFF
    mem[address + 3] = (val >> 24) & 0xFF


def execute(instruction):
    op = get_opcode(instruction)
    global pc
    global running

    # R - Type Instruction (ALL 10)
    if (op == 0x33):
        func3 = get_func3(instruction)
        func7 = get_func7(instruction)
        rd = get_rd(instruction)
        rs1 = get_rs1(instruction) 
        rs2 = get_rs2(instruction)

        # ADD
        if (func3 == 0x0 and func7 == 0x00):
            registers[rd] = u32(registers[rs1] + registers[rs2])
        # SUB
        elif (func3 == 0x0 and func7 == 0x20):
            registers[rd] = u32(registers[rs1] - registers[rs2])
        # XOR
        elif (func3 == 0x4 and func7 == 0x00):
            registers[rd] = u32(registers[rs1] ^ registers[rs2])
        # OR
        elif (func3 == 0x6 and func7 == 0x00):
            registers[rd] = u32(registers[rs1] | registers[rs2])
        # AND
        elif (func3 == 0x7 and func7 == 0x00):
            registers[rd] = u32(registers[rs1] & registers[rs2])
        # SLL
        elif (func3 == 0x1 and func7 == 0x00):
            registers[rd] = u32(registers[rs1] << (registers[rs2] & 0x1F))
        # SRL
        elif (func3 == 0x5 and func7 == 0x00):
            registers[rd] = u32(registers[rs1] >> (registers[rs2] & 0x1F))
        # SRA
        elif (func3 == 0x5 and func7 == 0x20):
            registers[rd] = u32(s32(registers[rs1]) >> (registers[rs2] & 0x1F))
        # SLT
        elif (func3 == 0x2 and func7 == 0x00):
            if (s32(registers[rs1]) < s32(registers[rs2])):
                registers[rd] = 1
            else:
                registers[rd] = 0
        # SLTU
        elif (func3 == 0x3 and func7 == 0x00):
            if (u32(registers[rs1]) < u32(registers[rs2])):
                registers[rd] = 1
            else:
                registers[rd] = 0
        else:
            raise Exception("Unknown R-type instruction.")
        pc += 4
        
    # I - Type Instruction

    # 0x13 Types (basic arithmetic/bitwise)
    elif (op == 0x13):
        imm = get_imm(instruction)
        func3 = get_func3(instruction)
        rs1 = get_rs1(instruction)
        rd = get_rd(instruction)
        func7 = get_func7(instruction)
        # ADDI
        if (func3 == 0x0):
            registers[rd] = u32(registers[rs1] + imm)
        # XORI
        elif (func3 == 0x4):
            registers[rd] = u32(registers[rs1] ^ imm)
        # ORI
        elif (func3 == 0x6):
            registers[rd] = u32(registers[rs1] | imm)
        # ANDI
        elif (func3 == 0x7):
            registers[rd] = u32(registers[rs1] & imm)
        # SLLI
        elif (func3 == 0x1 and func7 == 0x00):
            registers[rd] = u32(registers[rs1] << (imm & 0x1F)) # need final wrap since shift can cause overflow
        # SRLI
        elif (func3 == 0x5 and func7 == 0x00):
            registers[rd] = u32(registers[rs1]) >> (imm & 0x1F) # if rs1 is negative...need to make unsigned first
        # SRAI
        elif (func3 == 0x5 and func7 == 0x20):
            registers[rd] = u32(s32(registers[rs1]) >> (imm & 0x1F))
        # SLTI
        elif (func3 == 0x2):
            if (s32(registers[rs1]) < imm):
                registers[rd] = 1
            else:
                registers[rd] = 0
        # SLTIU
        elif (func3 == 0x3):
            if (u32(registers[rs1]) < u32(imm)):
                registers[rd] = 1
            else:
                registers[rd] = 0
        else:
            raise Exception("Unknown I-type instruction.")
        pc += 4



    # 0x03 (read/load into register)
    elif (op == 0x03):
        imm = get_imm(instruction)
        func3 = get_func3(instruction)
        rs1 = get_rs1(instruction)
        rd = get_rd(instruction)
        address = u32(registers[rs1] + imm)

        # Load Byte
        if (func3 == 0x0):
            value = mem[address]
            if (value & 0x80): # if value is negative
                value = value - 0x100
            registers[rd] = u32(value)
        elif (func3 == 0x1):
            value = mem[address] | mem[address + 1] << 8
            if (value & 0x8000):
                value = value - 0x10000
            registers[rd] = u32(value)
        elif (func3 == 0x2):
            registers[rd] = u32(mem[address] | mem[address + 1] << 8 | mem[address + 2] << 16 | mem[address + 3] << 24)

        elif (func3 == 0x04):
            value = u32(mem[address])
            registers[rd] = value
        elif (func3 == 0x05):
            registers[rd] = u32(mem[address] | mem[address + 1] << 8)

        else:
            raise Exception("Unknown load instruction.")
        pc += 4
        
    
    # S - Type Instructions
    elif (op == 0x23):
        imm_s = get_imm_s(instruction)
        rs1 = get_rs1(instruction)
        rs2 = get_rs2(instruction)
        func3 = get_func3(instruction)
        address = u32(registers[rs1] + imm_s)

        # SB
        if (func3 == 0x0):
            mem[address] = u32(registers[rs2]) & 0xFF
        # SH
        elif (func3 == 0x1):
            mem[address] = u32(registers[rs2]) & 0xFF
            mem[address + 1] = (u32(registers[rs2]) >> 8) & 0xFF
        # SW
        elif (func3 == 0x2):
            mem[address] = u32(registers[rs2]) & 0xFF
            mem[address + 1] = (u32(registers[rs2]) >> 8) & 0xFF
            mem[address + 2] = (u32(registers[rs2]) >> 16) & 0xFF
            mem[address + 3] = (u32(registers[rs2]) >> 24) & 0xFF
        else:
            raise Exception("Unknown store instructions.")
        pc += 4


    # B - Type Instructions
    elif (op == 0x63):
        imm_b = get_imm_b(instruction)
        rs2 = get_rs2(instruction)
        rs1 = get_rs1(instruction)
        func3 = get_func3(instruction)

        # BEQ
        if (func3 == 0x0):
            if (registers[rs1] == registers[rs2]):
                pc += imm_b
            else:
                pc += 4
        # BNE
        elif (func3 == 0x1):
            if (registers[rs1] != registers[rs2]):
                pc += imm_b
            else:
                pc += 4
        # BLT
        elif (func3 == 0x4):
            if (s32(registers[rs1]) < s32(registers[rs2])):
                pc += imm_b
            else:
                pc += 4
        # BGE
        elif (func3 == 0x5):
            if (s32(registers[rs1]) >= s32(registers[rs2])):
                pc += imm_b
            else:
                pc += 4
        # BLTU
        elif (func3 == 0x6):
            if (u32(registers[rs1]) < u32(registers[rs2])):
                pc += imm_b
            else:
                pc += 4
        # BGEU
        elif (func3 == 0x7):
            if (u32(registers[rs1]) >= u32(registers[rs2])):
                pc += imm_b
            else:
                pc += 4
        else:
            raise Exception("Unknown branch instruction")

    # J - Type Instruction
    # JAL
    elif (op == 0x6F):
        rd = get_rd(instruction)
        imm_j = get_imm_j(instruction)
        registers[rd] = u32(pc + 4)
        pc += imm_j
    
    # I - Type
    # JALR
    elif (op == 0x67):
        func3 = get_func3(instruction)
        if (func3 == 0x0):
            rd = get_rd(instruction)
            rs1 = get_rs1(instruction)
            imm_i = get_imm(instruction)

            return_address = pc + 4
            pc = u32(registers[rs1] + imm_i) & ~1
            registers[rd] = u32(return_address)
        else:
            raise Exception("Unknown JALR instruction.")
    # U - Type
    # LUI
    elif (op == 0x37):
        rd = get_rd(instruction)
        imm_u = get_imm_u(instruction)
        registers[rd] = u32(imm_u)
        pc += 4
    # AUIPC
    elif (op == 0x17):
        rd = get_rd(instruction)
        imm_u = get_imm_u(instruction)
        registers[rd] = u32(pc + imm_u)
        pc += 4
    
    # I - Type
    # ECALL/EBREAK...stop the program
    elif (op == 0x73):
        imm_i = get_imm(instruction)
        func3 = get_func3(instruction)

        if (func3 == 0x0 and imm_i == 0):
            running = False
        elif (func3 == 0x0 and imm_i == 1):
            running = False
        else:
            raise Exception("Unknown system instruction")
    else:
        raise Exception("Unknown opcode.")
    registers[0] = 0

    
# Load Program

def load_program(instruction, start_address=0):
    global pc
    pc = start_address

    address = start_address
    for i in instruction:
        store_word(address, i)
        address += 4



## add run loop.