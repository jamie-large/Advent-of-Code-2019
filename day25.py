NUM_PARAMS = {
    1: 3,
    2: 3,
    3: 1,
    4: 1,
    5: 2,
    6: 2,
    7: 3,
    8: 3,
    9: 1
}

class Machine:
    def __init__(self, code, inputs):
        self.code = code
        self.inputs = inputs
        self.index = 0
        self.relative_base = 0
        self.halted = False

    def run_machine(self):
        if self.index not in self.code:
            self.code[self.index] = 0
        opcode = self.code[self.index] % 100
        while opcode != 99:
            n_params = NUM_PARAMS[opcode]
            modes = [int(self.code[self.index] / (10 ** (i + 2))) % 10 for i in range(n_params)]
            parameters = [self.code.get(self.code.get(self.index + i + 1, 0), 0) if modes[i] == 0 else \
                          self.code.get(self.index + i + 1, 0) if modes[i] == 1 else \
                          self.code.get(self.code.get(self.index + i + 1, 0) + self.relative_base, 0) for i in range(n_params)]
            if opcode == 1:
                if modes[-1] == 0:
                    self.code[self.code.get(self.index + n_params, 0)] = parameters[0] + parameters[1]
                else:
                    self.code[self.code.get(self.index + n_params, 0) + self.relative_base] = parameters[0] + parameters[1]
            elif opcode == 2:
                if modes[-1] == 0:
                    self.code[self.code.get(self.index + n_params, 0)] = parameters[0] * parameters[1]
                else:
                    self.code[self.code.get(self.index + n_params, 0) + self.relative_base] = parameters[0] * parameters[1]
            elif opcode == 3:
                if len(self.inputs) == 0:
                    return
                if modes[-1] == 0:
                    self.code[self.code.get(self.index + n_params, 0)] = self.inputs.pop(0)
                else:
                    self.code[self.code.get(self.index + n_params, 0) + self.relative_base] = self.inputs.pop(0)
            elif opcode == 4:
                self.index += n_params + 1
                return parameters[0]
            elif opcode == 7:
                if modes[-1] == 0:
                    self.code[self.code.get(self.index + n_params, 0)] = 1 if parameters[0] < parameters[1] else 0
                else:
                    self.code[self.code.get(self.index + n_params, 0) + self.relative_base] = 1 if parameters[0] < parameters[1] else 0
            elif opcode == 8:
                if modes[-1] == 0:
                    self.code[self.code.get(self.index + n_params, 0)] = 1 if parameters[0] == parameters[1] else 0
                else:
                    self.code[self.code.get(self.index + n_params, 0) + self.relative_base] = 1 if parameters[0] == parameters[1] else 0
            elif opcode == 9:
                self.relative_base += parameters[0]

            if opcode == 5 and parameters[0] != 0:
                self.index = parameters[1]
            elif opcode == 6 and parameters[0] == 0:
                self.index = parameters[1]
            else:
                self.index += n_params + 1

            if self.index not in self.code:
                self.code[self.index] = 0
            opcode = self.code[self.index] % 100

        self.halted = True

    def add_input(self, val):
        self.inputs.append(val)


def solution_part1(fname="inputs/day25.txt"):
    with open(fname, "r") as f:
        code = {}
        code_arr = [int(x) for x in f.readline().split(",")]

        for i in range(len(code_arr)):
            code[i] = code_arr[i]

        m = Machine(code, [])

        while not m.halted:
            o = m.run_machine()
            if o is not None:
                print(chr(o), end="")
            else:
                inp = input()
                for c in inp:
                    m.add_input(ord(c))
                m.add_input(10)

solution_part1()
