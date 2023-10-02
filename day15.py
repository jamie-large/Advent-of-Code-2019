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

NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4

def solution_part1(fname="inputs/day15.txt"):
    with open(fname, "r") as f:
        code = {}
        code_arr = [int(x) for x in f.readline().split(",")]

        for i in range(len(code_arr)):
            code[i] = code_arr[i]

        m = Machine(code, [])

        output = 0
        position = (0, 0)

        floor_map = {
            (0, 0): "."
        }

        made_moves = []

        # Perform DFS
        while True:
            # Attempt to move North if unvisited
            if (position[0], position[1] + 1) not in floor_map:
                new_position = (position[0], position[1] + 1)
                m.add_input(NORTH)
                output = m.run_machine()

                if output == 0:
                    floor_map[new_position] = "#"
                elif output == 1 or output == 2:
                    floor_map[new_position] = "." if output == 1 else "O"
                    position = new_position
                    made_moves.append(NORTH)
            # Attempt to move East if unvisited
            elif (position[0] + 1, position[1]) not in floor_map:
                new_position = (position[0] + 1, position[1])
                m.add_input(EAST)
                output = m.run_machine()

                if output == 0:
                    floor_map[new_position] = "#"
                elif output == 1 or output == 2:
                    floor_map[new_position] = "." if output == 1 else "O"
                    position = new_position
                    made_moves.append(EAST)
            # Attempt to move South if unvisited
            elif (position[0], position[1] - 1) not in floor_map:
                new_position = (position[0], position[1] - 1)
                m.add_input(SOUTH)
                output = m.run_machine()

                if output == 0:
                    floor_map[new_position] = "#"
                elif output == 1 or output == 2:
                    floor_map[new_position] = "." if output == 1 else "O"
                    position = new_position
                    made_moves.append(SOUTH)
            # Attempt to move West if unvisited
            elif (position[0] - 1, position[1]) not in floor_map:
                new_position = (position[0] - 1, position[1])
                m.add_input(WEST)
                output = m.run_machine()

                if output == 0:
                    floor_map[new_position] = "#"
                elif output == 1 or output == 2:
                    floor_map[new_position] = "." if output == 1 else "O"
                    position = new_position
                    made_moves.append(WEST)
            # Backtrack if there's nowhere to go
            elif len(made_moves) > 0:
                previous_move = made_moves.pop()
                opposite = SOUTH if previous_move == NORTH else \
                           NORTH if previous_move == SOUTH else \
                           EAST if previous_move == WEST else WEST
                position = (position[0], position[1] + 1) if opposite == NORTH else \
                           (position[0], position[1] - 1) if opposite == SOUTH else \
                           (position[0] + 1, position[1]) if opposite == EAST else (position[0] - 1, position[1])

                m.add_input(opposite)
                m.run_machine()

            # If we can't backtrack, we've seen the whole field
            else:
                break

        # Perform BFS
        visited = set()
        processing = set([(0, 0)])
        positions = [((0, 0), 0)]
        while True:
            position, steps = positions.pop(0)
            processing.remove(position)
            visited.add(position)

            if floor_map[position] == "O":
                print(steps)
                return steps

            new_positions = [(position[0], position[1] + 1), (position[0], position[1] - 1), (position[0] + 1, position[1]), (position[0] - 1, position[1])]

            for np in new_positions:
                if np in floor_map and floor_map[np] != "#" and np not in processing and np not in visited:
                    processing.add(np)
                    positions.append((np, steps + 1))




def solution_part2(fname="inputs/day15.txt"):
    with open(fname, "r") as f:
        code = {}
        code_arr = [int(x) for x in f.readline().split(",")]

        for i in range(len(code_arr)):
            code[i] = code_arr[i]

        m = Machine(code, [])

        output = 0
        position = (0, 0)

        floor_map = {
            (0, 0): "."
        }

        made_moves = []

        # Perform DFS
        while True:
            # Attempt to move North if unvisited
            if (position[0], position[1] + 1) not in floor_map:
                new_position = (position[0], position[1] + 1)
                m.add_input(NORTH)
                output = m.run_machine()

                if output == 0:
                    floor_map[new_position] = "#"
                elif output == 1 or output == 2:
                    floor_map[new_position] = "." if output == 1 else "O"
                    position = new_position
                    made_moves.append(NORTH)
            # Attempt to move East if unvisited
            elif (position[0] + 1, position[1]) not in floor_map:
                new_position = (position[0] + 1, position[1])
                m.add_input(EAST)
                output = m.run_machine()

                if output == 0:
                    floor_map[new_position] = "#"
                elif output == 1 or output == 2:
                    floor_map[new_position] = "." if output == 1 else "O"
                    position = new_position
                    made_moves.append(EAST)
            # Attempt to move South if unvisited
            elif (position[0], position[1] - 1) not in floor_map:
                new_position = (position[0], position[1] - 1)
                m.add_input(SOUTH)
                output = m.run_machine()

                if output == 0:
                    floor_map[new_position] = "#"
                elif output == 1 or output == 2:
                    floor_map[new_position] = "." if output == 1 else "O"
                    position = new_position
                    made_moves.append(SOUTH)
            # Attempt to move West if unvisited
            elif (position[0] - 1, position[1]) not in floor_map:
                new_position = (position[0] - 1, position[1])
                m.add_input(WEST)
                output = m.run_machine()

                if output == 0:
                    floor_map[new_position] = "#"
                elif output == 1 or output == 2:
                    floor_map[new_position] = "." if output == 1 else "O"
                    position = new_position
                    made_moves.append(WEST)
            # Backtrack if there's nowhere to go
            elif len(made_moves) > 0:
                previous_move = made_moves.pop()
                opposite = SOUTH if previous_move == NORTH else \
                           NORTH if previous_move == SOUTH else \
                           EAST if previous_move == WEST else WEST
                position = (position[0], position[1] + 1) if opposite == NORTH else \
                           (position[0], position[1] - 1) if opposite == SOUTH else \
                           (position[0] + 1, position[1]) if opposite == EAST else (position[0] - 1, position[1])

                m.add_input(opposite)
                m.run_machine()

            # If we can't backtrack, we've seen the whole field
            else:
                break

        t = 0
        while any(floor_map[x] == "." for x in floor_map):
            oxygen_positions = [x for x in floor_map if floor_map[x] == "O"]
            for p in oxygen_positions:
                neighbors = [(p[0], p[1] + 1), (p[0], p[1] - 1), (p[0] + 1, p[1]), (p[0] -1, p[1])]
                for np in neighbors:
                    if np in floor_map and floor_map[np] == ".":
                        floor_map[np] = "O"
            t += 1

        print(t)

solution_part2()
