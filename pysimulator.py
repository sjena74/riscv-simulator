# building a riscv simulator in python for rv32I 
# using 32 registers and pc 


registers = [0] * 32
pc = 0
mem = bytearray(4096)
# each byte will be 2 hexes or 4 bits each

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
    return (instruction >> 20) & 0xFFF




def execute(instruction):
    op = get_opcode(instruction)

    # R - Type Instruction (ALL 10)
    if (op == 0x33):
        func3 = get_func3(instruction)
        func7 = get_func7(instruction)
        rd = get_rd(instruction)
        rs1 = get_rs1(instruction) 
        rs2 = get_rs2(instruction)

        # ADD
        if (func3 == 0x0 and func7 == 0x00):
            registers[rd] = registers[rs1] + registers[rs2]
        # SUB
        elif (func3 == 0x0 and func7 == 0x20):
            registers[rd] = registers[rs1] - registers[rs2]
        # XOR
        elif (func3 == 0x4 and func7 == 0x00):
            registers[rd] = registers[rs1] ^ registers[rs2]
        # OR
        elif (func3 == 0x6 and func7 == 0x00):
            registers[rd] = registers[rs1] | registers[rs2]
        # AND
        elif (func3 == 0x7 and func7 == 0x00):
            registers[rd] = registers[rs1] & registers[rs2]
        # SLL
        elif (func3 == 0x1 and func7 == 0x00):
            registers[rd] = registers[rs1] << registers[rs2]
        # SRL
        elif (func3 == 0x5 and func7 == 0x00):
            registers[rd] = registers[rs1] >> registers[rs2]
        # SRA
        elif (func3 == 0x5 and func7 == 0x20):
            registers[rd] = registers[rs1] >> registers[rs2]
        # SLT
        elif (func3 == 0x2 and func7 == 0x00):
            if (registers[rs1] < registers[rs2]):
                registers[rd] = 1
            else:
                registers[rd] = 0
        # SLTU
        elif (func3 == 0x3 and func7 == 0x00):
            if (registers[rs1] < registers[rs2]):
                registers[rd] = 1
            else:
                registers[rd] = 0
        
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
            registers[rd] = registers[rs1] + imm
        # XORI
        elif (func3 == 0x4):
            registers[rd] = registers[rs1] ^ imm
        # ORI
        elif (func3 == 0x6):
            registers[rd] = registers[rs1] | imm
        # ANDI
        elif (func3 == 0x7):
            registers[rd] = registers[rs1] & imm
        # SLLI
        elif (func3 == 0x1 and func7 == 0x00):
            registers[rd] = registers[rs1] << (imm & 0x1F)
        # SRLI
        elif (func3 == 0x5 and func7 == 0x00):
            registers[rd] = registers[rs1] >> (imm & 0x1F)
        # SRAI
        elif (func3 == 0x5 and func7 == 0x20):
            registers[rd] = registers[rs1] >> (imm & 0x1F)
        # SLTI
        elif (func3 == 0x2):
            if (registers[rs1] < imm):
                registers[rd] = 1
            else:
                registers[rd] = 0
        # SLTIU
        elif (func3 == 0x3):
            if (registers[rs1] < imm):
                registers[rd] = 1
            else:
                registers[rd] = 0



    # 0x03 (read/load into register)
    elif (op == 0x03):
        imm = get_imm(instruction)
        func3 = get_func3(instruction)
        rs1 = get_rs1(instruction)
        rd = get_rd(instruction)
        address = registers[rs1] + imm

        # Load Byte
        if (func3 == 0x0):
            registers[rd] = M[rs1 +]



        


        



