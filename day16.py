def solution_part1(fname="inputs/day16.txt"):
    with open(fname, "r") as f:
        input_list = [int(c) for c in f.readline()[:-1]]

        for _ in range(100):
            new_list = []
            for i in range(len(input_list)):
                pattern = [0 for _ in range(i+1)] + [1 for _ in range(i+1)] + [0 for _ in range(i+1)] + [-1 for _ in range(i+1)]
                value = 0
                for j in range(len(input_list)):
                    value += input_list[j] * pattern[(j + 1) % len(pattern)]
                new_list.append(abs(value) % 10)

            input_list = new_list

        print("".join([str(x) for x in input_list[:8]]))


def solution_part2(fname="inputs/day16.txt"):
    with open(fname, "r") as f:
        input_list = [int(c) for c in f.readline()[:-1]]
        input_list = input_list * 10000

        offset = int("".join([str(x) for x in input_list[:7]]))

        for _ in range(100):
            i = len(input_list) - 2
            while i >= offset:
                input_list[i] = abs(input_list[i] + input_list[i + 1]) % 10
                i -= 1


        print("".join([str(x) for x in input_list[offset:offset + 8]]))

solution_part2()
