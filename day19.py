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

def solution_part1(fname="inputs/day19.txt"):
    with open(fname, "r") as f:
        code = {}
        code_arr = [int(x) for x in f.readline().split(",")]

        for i in range(len(code_arr)):
            code[i] = code_arr[i]

        count = 0
        for i in range(50):
            for j in range(50):
                code_copy = {}
                for x in code:
                    code_copy[x] = code[x]
                m = Machine(code_copy, [])
                m.add_input(i)
                m.add_input(j)
                if (m.run_machine() == 1):
                    count += 1

        print(count)

def solution_part2(fname="inputs/day19.txt"):
    with open(fname, "r") as f:
        code = {}
        code_arr = [int(x) for x in f.readline().split(",")]

        for i in range(len(code_arr)):
            code[i] = code_arr[i]

        starting_position = (0, 1000)
        current_position = starting_position

        positions_map = {}

        while True:
            # count how many in a row we have for this row
            row_count = 0
            while True:
                if current_position not in positions_map:
                    code_copy = {}
                    for thing in code:
                        code_copy[thing] = code[thing]
                    m = Machine(code_copy, [])
                    m.add_input(current_position[0])
                    m.add_input(current_position[1])
                    positions_map[current_position] = m.run_machine()

                value = positions_map[current_position]
                if row_count > 0 and value == 0:
                    break
                elif value == 1:
                    row_count += 1

                current_position = (current_position[0] + 1, current_position[1])

            first_x = starting_position[0]
            while positions_map[(first_x, starting_position[1])] == 0:
                first_x += 1

            # if less than 100, continue to next row
            if row_count < 100:
                for x in range(starting_position[0], first_x + row_count + 1):
                    del positions_map[(x, starting_position[1])]
                starting_position = (first_x, starting_position[1] + 1)
                current_position = starting_position
                continue

            for x in range(first_x, first_x + row_count - 99):
                current_position = (x, starting_position[1] + 1)
                col_count = 1
                while True:
                    if current_position not in positions_map:
                        code_copy = {}
                        for thing in code:
                            code_copy[thing] = code[thing]
                        m = Machine(code_copy, [])
                        m.add_input(current_position[0])
                        m.add_input(current_position[1])
                        positions_map[current_position] = m.run_machine()

                    value = positions_map[current_position]
                    if value == 0:
                        break
                    col_count += 1

                    current_position = (current_position[0], current_position[1] + 1)

                if col_count >= 100:
                    BIG_MAP = []
                    print(x * 10000 + starting_position[1])
                    return

            # if we didn't find the full box, continue to the next row
            for x in range(starting_position[0], first_x + row_count + 1):
                del positions_map[(x, starting_position[1])]
            starting_position = (first_x, starting_position[1] + 1)
            current_position = starting_position

solution_part2()
