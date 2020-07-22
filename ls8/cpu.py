"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 255
        self.reg = [0] * 8
        self.pc = 0
        self.SP = 7
        self.reg[7] = 255

    
    def load(self, file_name):
        """Load a program into memory."""
        try:
            address = 0
            with open(file_name) as file:
                for line in file:
                    split_line = line.split('#')[0]
                    command = split_line.strip()
                    if command == '':
                        continue
                    instruction = int(command, 2)
                    self.ram[address] = instruction
                    address += 1
        
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} file not found")
            sys.exit()
                
    if len(sys.argv) < 2:
        print("Please pass in a second filename: ls8.py example/second_filename.py")
        sys.exit()

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        
        elif op == "MUL":
            # print(f"multiplying {self.reg[reg_a]} and {self.reg[reg_b]}")
            self.reg[reg_a] *= self.reg[reg_b]
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
    
    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value


    def run(self):
        """Run the CPU."""
        halted = False

        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010 
        PUSH = 0b01000101
        POP = 0b01000110

        while not halted:
            ir = self.ram[self.pc]     

            if ir == LDI:
                reg_num = self.ram_read(self.pc + 1)
                value = self.ram_read(self.pc + 2)
                self.reg[reg_num] = value
                self.pc += 3

            elif ir == PRN:
                reg_num = self.ram_read(self.pc + 1)
                print(self.reg[reg_num])
                self.pc += 2

            elif ir == HLT:
                halted = True
            
            elif ir == MUL:
                reg_num_a = self.ram_read(self.pc + 1)
                reg_num_b = self.ram_read(self.pc + 2)
                self.reg[reg_num_a] *= self.reg[reg_num_b]
                self.pc += 3
            elif ir == PUSH:
                # 1. Decrement the `SP`.
                # 2. Copy the value in the given register to the address pointed to by
                # `SP`.
                self.reg[7] = (self.reg[7] - 1) % 255
                self.SP = self.reg[7]
                register_address = self.ram[self.pc + 1]
                value = self.reg[register_address]
                self.ram[self.SP] = value
                self.pc += 2
            elif ir == POP:
                # 1. Copy the value from the address pointed to by `SP` to the given register.
                # 2. Increment `SP`.
                self.SP = self.reg[7]
                value = self.ram[self.SP]
                register_address = self.ram[self.pc + 1]
                self.reg[register_address] = value
                self.reg[7] = (self.SP + 1) % 255
                self.pc += 2

            else:
                print(f'Unknown instruction {ir} at address {self.pc}')
