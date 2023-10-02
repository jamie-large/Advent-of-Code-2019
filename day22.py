def solution_part1(fname="inputs/day22.txt"):
    with open(fname, "r") as f:
        N_CARDS = 10007
        card_position = 2019

        transformation = [1, 0]

        for line in f:
            if line[:-1] == "deal into new stack":
                transformation[0] = (transformation[0] * -1) % N_CARDS
                transformation[1] = (transformation[1] * -1 - 1) % N_CARDS
            elif line[:3] == "cut":
                n = int(line[4:])
                transformation[1]  = (transformation[1] - n) % N_CARDS
            else:
                n = int(line[20:])
                transformation[0] = (transformation[0] * n) % N_CARDS
                transformation[1] = (transformation[1] * n) % N_CARDS

        print((card_position * transformation[0] + transformation[1]) % N_CARDS)

def solution_part2(fname="inputs/day22.txt"):
    with open(fname, "r") as f:
        n = 119315717514047
        m = 101741582076661
        c = 2020

        a, b = 1, 0

        for line in f:
            if line[:-1] == "deal into new stack":
                la, lb = -1, -1
            elif line[:3] == "cut":
                la, lb = 1, -1 * int(line[4:])
            else:
                la, lb = int(line[20:]), 0
            a = (la * a) % n
            b = (la * b + lb) % n

        Ma = pow(a, m, n)
        Mb = (b * (Ma - 1) * inv(a-1, n)) % n

        print(((c - Mb) * inv(Ma, n)) % n)

def inv(a, n):
    return pow(a, n-2, n)

solution_part2()
