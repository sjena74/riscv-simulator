# RV32I RISC-V Simulator in Python

This project is a simple RV32I RISC-V simulator written in Python. It models the basic state of a 32-bit RISC-V processor, including 32 registers, a program counter, and byte-addressed memory.

The main goal of this project is to better understand how RISC-V machine instructions are decoded and executed at a low level.

## Features

- 32 general-purpose registers
- Program counter (`pc`)
- Byte-addressed memory using `bytearray`
- Little-endian load/store behavior
- Signed and unsigned 32-bit helper functions
- Instruction decoding using bit masks and shifts
- Basic exception handling for unknown instructions
- `x0` is kept hardwired to zero

## Supported Instructions

### R-Type

- `ADD`
- `SUB`
- `XOR`
- `OR`
- `AND`
- `SLL`
- `SRL`
- `SRA`
- `SLT`
- `SLTU`

### I-Type Arithmetic

- `ADDI`
- `XORI`
- `ORI`
- `ANDI`
- `SLLI`
- `SRLI`
- `SRAI`
- `SLTI`
- `SLTIU`

### Loads

- `LB`
- `LH`
- `LW`
- `LBU`
- `LHU`

### Stores

- `SB`
- `SH`
- `SW`

### Branches

- `BEQ`
- `BNE`
- `BLT`
- `BGE`
- `BLTU`
- `BGEU`

### Jumps

- `JAL`
- `JALR`

### U-Type

- `LUI`
- `AUIPC`

### System

- `ECALL`
- `EBREAK`

## How It Works

The simulator stores the CPU state with:

```python
registers = [0] * 32
pc = 0
mem = bytearray(4096)
