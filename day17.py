class Comp:

    def __init__(self):
        self.program = self.read()
        self.pointer = 0

    def read(self):
        with open('data/input_day17.txt') as f:
            self.A = int(f.readline().strip().split(': ')[-1])
            self.B = int(f.readline().strip().split(': ')[-1])
            self.C = int(f.readline().strip().split(': ')[-1])
            f.readline()
            program = f.readline().strip().split(': ')[-1].split(',')
        return [int(i) for i in program]

    def exec(self):
        output = []
        while self.pointer < len(self.program):
            opcode = self.program[self.pointer]
            if opcode == 3:
                pointer = self.pointer
            else:
                pointer = -1
            operand = self.program[self.pointer+1]
            out = self.exec_one(opcode, operand)
            if opcode == 3 and self.pointer == pointer:
                raise ValueError('infinite loop')
            if out is not None:
                output.append(out)
        return output

    def format_output(self, output):
        return ','.join([str(i) for i in output])

    def dec_to_bin(self, dec):
        return f'{dec:b}'

    def bin_to_dec(self, bin):
        return int(bin, 2)

    def xor(self, v1, v2):
        v1 = self.dec_to_bin(v1)
        v2 = self.dec_to_bin(v2)
        # pad 0s
        while len(v1) != len(v2):
            if len(v1) < len(v2):
                v1 = '0' + v1
            else:
                v2 = '0' + v2
        # xor
        new = ''
        for i1, i2 in zip(v1, v2):
            if i1 == i2:
                new = new + '0'
            else:
                new = new + '1'
        return self.bin_to_dec(new)

    def exec_one(self, opcode, operand):
        if opcode == 0:
            return self.adv(operand)
        elif opcode == 1:
            return self.bxl(operand)
        elif opcode == 2:
            return self.bst(operand)
        elif opcode == 3:
            return self.jnz(operand)
        elif opcode == 4:
            return self.bxc(operand)
        elif opcode == 5:
            return self.out(operand)
        elif opcode == 6:
            return self.bdv(operand)
        elif opcode == 7:
            return self.cdv(operand)

    def combo_operand(self, operand):
        if operand in [0,1,2,3]:
            return operand
        elif operand == 4:
            return self.A
        elif operand == 5:
            return self.B
        elif operand == 6:
            return self.C

    def adv(self, operand):
        self.A = int(self.A/2**self.combo_operand(operand))
        self.pointer += 2

    def bxl(self, operand):
        self.B = self.xor(operand, self.B)
        self.pointer += 2

    def bst(self, operand):
        self.B = self.combo_operand(operand) % 8
        self.pointer += 2

    def jnz(self, operand):
        if self.A != 0:
            self.pointer = operand
        else:
            self.pointer += 2

    def bxc(self, operand):
        self.B = self.xor(self.B, self.C)
        self.pointer += 2

    def out(self, operand):
        self.pointer += 2
        return self.combo_operand(operand) % 8

    def bdv(self, operand):
        self.B = int(self.A/2**self.combo_operand(operand))
        self.pointer += 2

    def cdv(self, operand):
        self.C = int(self.A/2**self.combo_operand(operand))
        self.pointer += 2

comp = Comp()
print('challenge 1', comp.format_output(comp.exec()))
