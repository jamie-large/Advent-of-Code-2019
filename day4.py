def solution_part1(fname):
    with open(fname, "r") as f:
        [min_val, max_val] = [int(x) for x in f.readline().split("-")]
        count = 0
        for i in range(min_val, max_val + 1):
            if is_valid(i):
                count += 1
        print(count)
        return count



def is_valid(num):
    str_num = str(num)
    found_double = False
    for i in range(len(str_num) - 1):
        if str_num[i] > str_num[i+1]:
            return False
        if str_num[i] == str_num[i+1]:
            found_double = True

    return found_double


def solution_part2(fname):
    with open(fname, "r") as f:
        [min_val, max_val] = [int(x) for x in f.readline().split("-")]
        count = 0
        for i in range(min_val, max_val + 1):
            if is_valid_2(i):
                count += 1
        print(count)
        return count

def is_valid_2(num):
    str_num = str(num)
    num_counts = [0 for _ in range(10)]
    for i in range(len(str_num) - 1):
        if str_num[i] > str_num[i+1]:
            return False
        num_counts[int(str_num[i])] += 1
    num_counts[int(str_num[-1])] += 1

    return any(x == 2 for x in num_counts)

solution_part2("inputs/day4.txt")

