"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        
        self.pc = 0
        self.ram = [0] * 255
        self.reg = [0] * 8
        self.sp = 7
        self.flag = 0b11111111




    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]
        with open(sys.argv[1]) as f:
            for line in f:
                comment_split = line.strip().split("#")
                num = comment_split[0]
                if num == "":
                    continue
                x = int(num, 2)
                # print(f"{x:08b}: {x:d}")
                self.ram[address] = x
                address += 1
        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MAD):
        self.ram[MAR] = MAD

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            print("add")
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            print("mul")
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP":
            if reg_a is reg_b:
                self.flag = 0b00000001
            elif reg_a < reg_b:
                self.flag = 0b00000100
            elif reg_a > reg_b:
                self.flag = 0b00000010
            else:
                self.flag = 0b00000000
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        
        running = True
        LDI = 0b10000010
        PRN = 0b01000111
        HALT = 0b00000001
        ADD = 0b10101000
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110
        CALL = 0b01010000
        RET = 0b01010000
        CMP = 0b10100111
        JEQ = 0b01010101
        JMP = 0b01010100
        JNE = 0b01010110


        while running:
            instruction = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            increment = (instruction >> 6) + 1
            print("Increment",increment)
            if instruction == LDI:
                print("LDI", operand_b)
                self.reg[operand_a] = operand_b
                self.pc += increment
            elif instruction == PRN:
                print(self.reg[operand_a])
                self.pc += increment
            elif instruction == HALT:
                running = False
            elif instruction == ADD:
                self.alu("ADD", operand_a, operand_b)
                self.pc += increment
            elif instruction == MUL:
                self.alu("MUL", operand_a, operand_b)
                self.pc += increment
            elif instruction == PUSH:
                self.sp -= 1
                value = self.reg[operand_a]
                self.ram_write(self.sp, value)
                self.pc += increment
            elif instruction == POP:
                print("pop")
                value = self.ram_read(self.sp)
                self.reg[operand_a] = value
                self.sp += 1
                self.pc += increment
            elif instruction == CALL:
                print("call")
                print(self.ram[self.sp])
                self.ram[self.sp] = increment
                print(self.ram[self.sp])

                self.pc = operand_a
            elif instruction == RET:
                print("RET")
                self.pc = self.ram[self.sp]
            elif instruction == CMP:
                self.alu("CMP", operand_a, operand_b)
                self.pc += 3
            elif instruction == JEQ:
                if self.flag == (self.flag & 0b00000001):
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2
            elif instruction == JNE:
                if self.flag != 0b00000001:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2
            elif instruction == JMP:
                self.pc = self.reg[operand_a]
            else:
                print("Nothing")