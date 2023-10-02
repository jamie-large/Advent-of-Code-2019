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

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

DIRECTIONS = [NORTH, EAST, SOUTH, WEST]

def solution_part1(fname="inputs/day11.txt"):
    with open(fname, "r") as f:
        code = {}
        code_arr = [int(x) for x in f.readline().split(",")]

        for i in range(len(code_arr)):
            code[i] = code_arr[i]

        m = Machine(code, [])
        robot_position = (0, 0)
        robot_direction = NORTH
        tile_colors = {}
        painted_tiles = set()
        while not m.halted:
            m.add_input(tile_colors.get(robot_position, 0))
            new_color = m.run_machine()
            new_direction = m.run_machine()

            # paint tile
            tile_colors[robot_position] = new_color
            painted_tiles.add(robot_position)

            # rotate
            if new_direction == 0:
                robot_direction = DIRECTIONS[DIRECTIONS.index(robot_direction) - 1]
            else:
                robot_direction = DIRECTIONS[(DIRECTIONS.index(robot_direction) + 1) % 4]

            # move
            if robot_direction == NORTH:
                robot_position = (robot_position[0], robot_position[1] + 1)
            elif robot_direction == EAST:
                robot_position = (robot_position[0] + 1, robot_position[1])
            elif robot_direction == SOUTH:
                robot_position = (robot_position[0], robot_position[1] - 1)
            elif robot_direction == WEST:
                robot_position = (robot_position[0] - 1, robot_position[1])

        print(len(painted_tiles))

def solution_part2(fname="inputs/day11.txt"):
    with open(fname, "r") as f:
        code = {}
        code_arr = [int(x) for x in f.readline().split(",")]

        for i in range(len(code_arr)):
            code[i] = code_arr[i]

        m = Machine(code, [])
        robot_position = (0, 0)
        robot_direction = NORTH
        tile_colors = {}
        painted_tiles = set()

        tile_colors[(0,0)] = 1
        while not m.halted:
            m.add_input(tile_colors.get(robot_position, 0))
            new_color = m.run_machine()
            new_direction = m.run_machine()

            # paint tile
            tile_colors[robot_position] = new_color
            painted_tiles.add(robot_position)

            # rotate
            if new_direction == 0:
                robot_direction = DIRECTIONS[DIRECTIONS.index(robot_direction) - 1]
            else:
                robot_direction = DIRECTIONS[(DIRECTIONS.index(robot_direction) + 1) % 4]

            # move
            if robot_direction == NORTH:
                robot_position = (robot_position[0], robot_position[1] + 1)
            elif robot_direction == EAST:
                robot_position = (robot_position[0] + 1, robot_position[1])
            elif robot_direction == SOUTH:
                robot_position = (robot_position[0], robot_position[1] - 1)
            elif robot_direction == WEST:
                robot_position = (robot_position[0] - 1, robot_position[1])

        min_x = 1000
        max_x = -1000
        min_y = 1000
        max_y = -1000

        for pos in painted_tiles:
            if pos[0] < min_x:
                min_x = pos[0]
            if pos[0] > max_x:
                max_x = pos[0]
            if pos[1] < min_y:
                min_y = pos[1]
            if pos[1] > max_y:
                max_y = pos[1]

        grid = [["." for _ in range(max_x - min_x + 1)] for _ in range(max_y - min_y + 1)]
        for pos in painted_tiles:
            if tile_colors[pos] == 1:
                grid[pos[1] - min_y][pos[0] - min_x] = "#"

        for i in range(len(grid) - 1, -1, -1):
            print("".join([str(x) for x in grid[i]]))


solution_part2()
