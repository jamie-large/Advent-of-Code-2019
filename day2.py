def solution_part1(fname):
    with open(fname, "r") as f:
        code = [int(x) for x in f.readline().split(",")]
        code[1] = 12
        code[2] = 2
        index = 0
        while code[index] != 99:
            if code[index] == 1:
                code[code[index + 3]] = code[code[index + 1]] + code[code[index + 2]]
            elif code[index] == 2:
                code[code[index + 3]] = code[code[index + 1]] * code[code[index + 2]]
            index += 4

        print(code[0])

def solution_part2(fname):
    with open(fname, "r") as f:
        original_code = [int(x) for x in f.readline().split(",")]
        for noun in range(100):
            for verb in range(100):
                code = [x for x in original_code]
                code[1] = noun
                code[2] = verb
                index = 0
                while index < len(code) and code[index] != 99:
                    if code[index] == 1:
                        code[code[index + 3]] = code[code[index + 1]] + code[code[index + 2]]
                    elif code[index] == 2:
                        code[code[index + 3]] = code[code[index + 1]] * code[code[index + 2]]
                    index += 4
                if index < len(code) and code[0] == 19690720:
                    print(100 * noun + verb)
                    return

solution_part2("inputs/day2.txt")
