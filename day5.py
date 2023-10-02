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

def solution_part1(fname):
    with open(fname, "r") as f:
        code = [int(x) for x in f.readline().split(",")]
        inputs = [1]
        inputs_index = 0
        index = 0
        opcode = code[index] % 100
        while opcode != 99:
            modes = [int(code[index] / (10 ** (i + 2))) % 10 for i in range(NUM_PARAMS[opcode])]
            parameters = [code[code[index + i + 1]] if modes[i] == 0 else code[index + i + 1] for i in range(NUM_PARAMS[opcode])]

            if opcode == 1:
                code[code[index + 3]] = parameters[0] + parameters[1]
            elif opcode == 2:
                code[code[index + 3]] = parameters[0] * parameters[1]
            elif opcode == 3:
                code[code[index + 1]] = inputs[inputs_index]
                inputs_index += 1
            elif opcode == 4:
                print(str(parameters[0]))

            index += NUM_PARAMS[opcode] + 1
            opcode = code[index] % 100

def solution_part2(fname):
    with open(fname, "r") as f:
        code = [int(x) for x in f.readline().split(",")]
        inputs = [5]
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
                print(str(parameters[0]))
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

solution_part2("inputs/day5.txt")
