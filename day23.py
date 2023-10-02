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


def solution_part1(fname="inputs/day23.txt"):
    with open(fname, "r") as f:
        code = {}
        code_arr = [int(x) for x in f.readline().split(",")]

        for i in range(len(code_arr)):
            code[i] = code_arr[i]

        computers: list[Machine] = []

        for i in range(50):
            code_copy = {}
            for x in code:
                code_copy[x] = code[x]
            computers.append(Machine(code_copy, [i, -1]))

        while True:
            for i in range(50):
                if len(computers[i].inputs) == 0:
                    computers[i].add_input(-1)
                addr = computers[i].run_machine()
                if addr is None:
                    continue
                X = computers[i].run_machine()
                Y = computers[i].run_machine()
                if addr == 255:
                    print(Y)
                    return

                if addr < len(computers):
                    computers[addr].add_input(X)
                    computers[addr].add_input(Y)

def solution_part2(fname="inputs/day23.txt"):
    with open(fname, "r") as f:
        code = {}
        code_arr = [int(x) for x in f.readline().split(",")]

        for i in range(len(code_arr)):
            code[i] = code_arr[i]

        computers: list[Machine] = []

        NAT = ()

        last_delivered = None

        for i in range(50):
            code_copy = {}
            for x in code:
                code_copy[x] = code[x]
            computers.append(Machine(code_copy, [i, -1]))

        while True:
            sent = False
            for i in range(50):
                if len(computers[i].inputs) == 0:
                    computers[i].add_input(-1)
                addr = computers[i].run_machine()
                if addr is None:
                    continue

                sent = True
                X = computers[i].run_machine()
                Y = computers[i].run_machine()

                if addr == 255:
                    NAT = (X, Y)

                if addr < len(computers):
                    computers[addr].add_input(X)
                    computers[addr].add_input(Y)

            if all([len(c.inputs) == 0 for c in computers]) and not sent:
                if NAT[1] == last_delivered:
                    print(NAT[1])
                    return
                computers[0].add_input(NAT[0])
                computers[0].add_input(NAT[1])
                last_delivered = NAT[1]


solution_part2()
