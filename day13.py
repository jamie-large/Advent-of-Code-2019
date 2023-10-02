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


def solution_part1(fname="inputs/day13.txt"):
    with open(fname, "r") as f:
        code = {}
        code_arr = [int(x) for x in f.readline().split(",")]

        for i in range(len(code_arr)):
            code[i] = code_arr[i]

        code[0] = 2

        m = Machine(code, [])
        outputs = []

        while not m.halted:
            outputs.append(m.run_machine())

        outputs.pop(-1)

        grid = {}
        i = 0
        while i < len(outputs):
            grid[(outputs[i], outputs[i+1])] = outputs[i+2]
            i += 3

        print(outputs)

        print(list(grid.values()).count(2))


READING = 0
PLAYING = 1

def solution_part2(fname="inputs/day13.txt"):
    with open(fname, "r") as f:
        code = {}
        code_arr = [int(x) for x in f.readline().split(",")]

        for i in range(len(code_arr)):
            code[i] = code_arr[i]

        code[0] = 2

        m = Machine(code, [])

        grid = []
        drawing_instructions = []

        current_score = 0

        ball_x = 0
        paddle_x = 0
        while not m.halted:
            x = m.run_machine()
            y = m.run_machine()
            id = m.run_machine()

            if id == 4:
                ball_x = x
                if paddle_x < ball_x:
                    m.add_input(1)
                elif paddle_x == ball_x:
                    m.add_input(0)
                else:
                    m.add_input(-1)

            if id == 3:
                paddle_x = x

            if x == -1:
                current_score = id
                max_x = 0
                max_y = 0
                for ins in drawing_instructions:
                    if ins[0] > max_x:
                        max_x = ins[0]
                    if ins[1] > max_y:
                        max_y = ins[1]

                grid = [[" " for _ in range(max_x + 1)] for _ in range(max_y + 1)]

                for ins in drawing_instructions:
                    char = " " if ins[2] == 0 else \
                            "X" if ins[2] == 1 else \
                            "B" if ins[2] == 2 else \
                            "_" if ins[2] == 3 else "O"
                    grid[ins[1]][ins[0]] = char

                if sum([x.count("B") for x in grid]) == 0:
                    print(current_score)
                    return

            else:
                drawing_instructions.append((x, y, id))

solution_part2()
