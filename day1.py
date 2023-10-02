def solution_part1(fname):
    with open(fname, "r") as f:
        result = 0
        for line in f:
            result += fuel_required(int(line))
        print(result)
        return result

def solution_part2(fname):
    with open(fname, "r") as f:
        result = 0
        for line in f:
            result += fuel_required2(int(line))
        print(result)
        return result

def fuel_required(mass):
    return int(mass / 3) - 2

fuel_needed_map = {}
def fuel_required2(mass):
    if mass in fuel_needed_map:
        return fuel_needed_map[mass]
    result = int(mass / 3) - 2
    if (result <= 0):
        fuel_needed_map[mass] = 0
        return 0
    else:
        result = result + fuel_required2(result)
        fuel_needed_map[mass] = result
        return result

solution_part2("inputs/day1.txt")
