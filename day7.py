NUM_PARAMS = {
    1: 3,
    2: 3,
    3: 1,
    4: 1,
    5: 2,
    6: 2,
    7: 3,
    8: 3
}

def run_machine(code, inputs):
    inputs_index = 0
    index = 0
    opcode = code[index] % 100
    while opcode != 99:
        n_params = NUM_PARAMS[opcode]
        modes = [int(code[index] / (10 ** (i + 2))) % 10 for i in range(n_params)]
        parameters = [code[code[index + i + 1]] if modes[i] == 0 else code[index + i + 1] for i in range(n_params)]

        if opcode == 1:
            code[code[index + n_params]] = parameters[0] + parameters[1]
        elif opcode == 2:
            code[code[index + n_params]] = parameters[0] * parameters[1]
        elif opcode == 3:
            code[code[index + n_params]] = inputs[inputs_index]
            inputs_index += 1
        elif opcode == 4:
            return parameters[0]
        elif opcode == 7:
            code[code[index + n_params]] = 1 if parameters[0] < parameters[1] else 0
        elif opcode == 8:
            code[code[index + n_params]] = 1 if parameters[0] == parameters[1] else 0

        if opcode == 5 and parameters[0] != 0:
            index = parameters[1]
        elif opcode == 6 and parameters[0] == 0:
            index = parameters[1]
        else:
            index += n_params + 1
        opcode = code[index] % 100

def solution_part1(fname="inputs/day7.txt"):
    with open(fname, "r") as f:
        original_code = [int(x) for x in f.readline().split(",")]
        possibilities = [(i, j, k, l, m) for i in range(5) for j in range(5) for k in range(5) for l in range(5) for m in range(5)
                         if i != j and i != k and i != l and i != m and j != k and j != l and j != m and k != l and k != m and l != m]
        max_output = -9999999999999
        for p in possibilities:
            out = run_machine([x for x in original_code], [p[0], 0])
            out = run_machine([x for x in original_code], [p[1], out])
            out = run_machine([x for x in original_code], [p[2], out])
            out = run_machine([x for x in original_code], [p[3], out])
            out = run_machine([x for x in original_code], [p[4], out])
            if out > max_output:
                max_output = out

        print(max_output)

class Machine:
    def __init__(self, code, inputs):
        self.code = code
        self.inputs = inputs
        self.index = 0
        self.halted = False

    def run_machine(self):
        opcode = self.code[self.index] % 100
        while opcode != 99:
            n_params = NUM_PARAMS[opcode]
            modes = [int(self.code[self.index] / (10 ** (i + 2))) % 10 for i in range(n_params)]
            parameters = [self.code[self.code[self.index + i + 1]] if modes[i] == 0 else self.code[self.index + i + 1] for i in range(n_params)]

            if opcode == 1:
                self.code[self.code[self.index + n_params]] = parameters[0] + parameters[1]
            elif opcode == 2:
                self.code[self.code[self.index + n_params]] = parameters[0] * parameters[1]
            elif opcode == 3:
                self.code[self.code[self.index + n_params]] = self.inputs.pop(0)
            elif opcode == 4:
                self.index += n_params + 1
                return parameters[0]
            elif opcode == 7:
                self.code[self.code[self.index + n_params]] = 1 if parameters[0] < parameters[1] else 0
            elif opcode == 8:
                self.code[self.code[self.index + n_params]] = 1 if parameters[0] == parameters[1] else 0

            if opcode == 5 and parameters[0] != 0:
                self.index = parameters[1]
            elif opcode == 6 and parameters[0] == 0:
                self.index = parameters[1]
            else:
                self.index += n_params + 1
            opcode = self.code[self.index] % 100

        self.halted = True

    def add_input(self, val):
        self.inputs.append(val)

def solution_part2(fname="inputs/day7.txt"):
    with open(fname, "r") as f:
        original_code = [int(x) for x in f.readline().split(",")]
        possibilities = [(i, j, k, l, m) for i in range(5,10) for j in range(5,10) for k in range(5,10) for l in range(5,10) for m in range(5,10)
                         if i != j and i != k and i != l and i != m and j != k and j != l and j != m and k != l and k != m and l != m]
        max_output = -9999999999999
        for p in possibilities:
            A = Machine([x for x in original_code], [p[0]])
            B = Machine([x for x in original_code], [p[1]])
            C = Machine([x for x in original_code], [p[2]])
            D = Machine([x for x in original_code], [p[3]])
            E = Machine([x for x in original_code], [p[4]])

            out = new_out = 0
            while not E.halted:
                out = new_out
                A.add_input(new_out)
                B.add_input(A.run_machine())
                C.add_input(B.run_machine())
                D.add_input(C.run_machine())
                E.add_input(D.run_machine())
                new_out = E.run_machine()

            if out > max_output:
                max_output = out

        print(max_output)

solution_part2()
