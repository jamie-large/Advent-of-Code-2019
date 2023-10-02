import math

class Moon:
    def __init__(self, position):
        self.position = position
        self.velocity = [0, 0, 0]

    def __repr__(self):
        return f"pos={self.position}, vel={self.velocity})"

    def __str__(self):
        return f"{self.position}{self.velocity}"

def solution_part1(fname="inputs/day12.txt"):
    with open(fname, "r") as f:
        moons = [Moon([int(x[3:]) for x in line[:-2].split(",")]) for line in f]

        for _ in range(1000):
            velocity_changes = [[0, 0, 0] for _ in range(4)]
            for i in range(4):
                for j in range(i+1, 4):
                    for k in range(3):
                        if moons[i].position[k] > moons[j].position[k]:
                            velocity_changes[i][k] -= 1
                            velocity_changes[j][k] += 1
                        elif moons[i].position[k] < moons[j].position[k]:
                            velocity_changes[i][k] += 1
                            velocity_changes[j][k] -= 1

                for j in range(3):
                    moons[i].velocity[j] += velocity_changes[i][j]
                    moons[i].position[j] += moons[i].velocity[j]


        total_energy = sum([sum([abs(x) for x in m.position]) * sum([abs(x) for x in m.velocity]) for m in moons])

        print(total_energy)

def solution_part2(fname="inputs/day12.txt"):
    with open(fname, "r") as f:
        moons = [Moon([int(x[3:]) for x in line[:-2].split(",")]) for line in f]

        seen_positions = [set(), set(), set()]
        found = [-1, -1, -1]

        t = 0
        while any(x == -1 for x in found):
            positions = [(moons[0].position[i], moons[1].position[i], moons[2].position[i], moons[3].position[i], \
                          moons[0].velocity[i], moons[1].velocity[i], moons[2].velocity[i], moons[3].velocity[i]) for i in range(3)]
            for i in range(3):
                if found[i] == -1 and positions[i] in seen_positions[i]:
                    found[i] = t
                elif found[i] == -1:
                    seen_positions[i].add(positions[i])

            velocity_changes = [[0, 0, 0] for _ in range(4)]
            for i in range(4):
                for j in range(i+1, 4):
                    for k in range(3):
                        if moons[i].position[k] > moons[j].position[k]:
                            velocity_changes[i][k] -= 1
                            velocity_changes[j][k] += 1
                        elif moons[i].position[k] < moons[j].position[k]:
                            velocity_changes[i][k] += 1
                            velocity_changes[j][k] -= 1

                for j in range(3):
                    moons[i].velocity[j] += velocity_changes[i][j]
                    moons[i].position[j] += moons[i].velocity[j]

            t += 1

        print(math.lcm(*found))

solution_part2()
