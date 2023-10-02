def solution_part1(fname):
    with open(fname, "r") as f:
        wire = 1
        crosses = set()
        wire_locations = set()
        for line in f:
            instructions = line.split(",")
            position = [0, 0]
            for inst in instructions:
                val = int(inst[1:])
                if inst[0] == "D":
                    positions = [(position[0], position[1] - i) for i in range(1, val + 1)]
                    position = [position[0], position[1] - val]
                elif inst[0] == "U":
                    positions = [(position[0], position[1] + i) for i in range(1, val + 1)]
                    position = [position[0], position[1] + val]
                elif inst[0] == "L":
                    positions = [(position[0] - i, position[1]) for i in range(1, val + 1)]
                    position = [position[0] - val, position[1]]
                elif inst[0] == "R":
                    positions = [(position[0] + i, position[1]) for i in range(1, val + 1)]
                    position = [position[0] + val, position[1]]

                for p in positions:
                    if wire == 1:
                        wire_locations.add(p)
                    else:
                        if p in wire_locations:
                            crosses.add(p)

            wire += 1

        print(min([abs(x) + abs(y) for (x, y) in crosses]))




def solution_part2(fname):
    with open(fname, "r") as f:
        wire = 1
        crosses = set()
        wire_locations = {}
        for line in f:
            instructions = line.split(",")
            position = [0, 0]
            steps = 0
            for inst in instructions:
                val = int(inst[1:])
                if inst[0] == "D":
                    positions = [(position[0], position[1] - i, steps + i) for i in range(1, val + 1)]
                    position = [position[0], position[1] - val]
                elif inst[0] == "U":
                    positions = [(position[0], position[1] + i, steps + i) for i in range(1, val + 1)]
                    position = [position[0], position[1] + val]
                elif inst[0] == "L":
                    positions = [(position[0] - i, position[1], steps + i) for i in range(1, val + 1)]
                    position = [position[0] - val, position[1]]
                elif inst[0] == "R":
                    positions = [(position[0] + i, position[1], steps + i) for i in range(1, val + 1)]
                    position = [position[0] + val, position[1]]

                for p in positions:
                    if wire == 1 and (p[0], p[1]) not in wire_locations:
                        wire_locations[(p[0], p[1])] = p[2]
                    elif wire == 2 and (p[0], p[1]) in wire_locations:
                        crosses.add(wire_locations[(p[0], p[1])] + p[2])
                steps += val

            wire += 1

        print(min(crosses))


solution_part2("inputs/day3.txt")
