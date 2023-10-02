from fractions import Fraction

def solution_part1(fname="inputs/day10.txt"):
    with open(fname, "r") as f:
        space_map = [line[:-1] for line in f.readlines()]
        asteroids = [(i, j) for i in range(len(space_map[0])) for j in range(len(space_map)) if space_map[j][i] == "#"]
        print(max([calculate_asteroids_seen(a[0], a[1], asteroids) for a in asteroids]))


def calculate_asteroids_seen(x, y, asteroids):
    vectors = set()
    cardinal_checks = [False, False, False, False]
    for (i, j) in asteroids:
        if i == x and j == y:
            continue
        if j - y == 0:
            if i - x > 0:
                cardinal_checks[0] = True
            else:
                cardinal_checks[1] = True
            continue

        if i - x == 0:
            if j - y > 0:
                cardinal_checks[2] = True
            else:
                cardinal_checks[3] = True
            continue

        v = (Fraction(i - x, j - y), 1 if i-x > 0 else -1)
        if v not in vectors:
            vectors.add(v)
    return len(vectors) + len([x for x in cardinal_checks if x])



def solution_part2(fname="inputs/day10.txt"):
    with open(fname, "r") as f:
        space_map = [line[:-1] for line in f.readlines()]
        asteroids = [(i, j) for i in range(len(space_map[0])) for j in range(len(space_map)) if space_map[j][i] == "#"]
        seen_asteroids = {}
        for a in asteroids:
            seen_asteroids[a] = calculate_asteroids_seen(a[0], a[1], asteroids)

        station_location = None
        max_seen = 0
        for a in asteroids:
            if seen_asteroids[a] > max_seen:
                max_seen = seen_asteroids[a]
                station_location = a

        asteroids_set = set(asteroids)
        asteroids_set.remove(station_location)

        (x, y) = station_location

        destroyed = []
        while len(destroyed) < 200:
            vectors = set()
            cardinal_checks = [False, False, False, False]
            for (i, j) in asteroids_set:
                if j - y == 0:
                    if i - x > 0:
                        cardinal_checks[0] = True
                    else:
                        cardinal_checks[1] = True
                    continue

                if i - x == 0:
                    if j - y > 0:
                        cardinal_checks[2] = True
                    else:
                        cardinal_checks[3] = True
                    continue

                v = (Fraction(i - x, j - y), 1 if i-x > 0 else -1)
                if v not in vectors:
                    vectors.add(v)

            # destroy above if exists
            if cardinal_checks[3]:
                for i in range(y - 1, -1, -1):
                    if (x, i) in asteroids_set:
                        asteroids_set.remove((x,i))
                        destroyed.append((x, i))
                        break

            # go through NE vectors
            current_vectors = [v[0] for v in vectors if v[1] == 1 and v[0] < 0]
            current_vectors.sort(reverse=True)
            for v in current_vectors:
                pos = station_location
                while pos not in asteroids_set:
                    pos = (pos[0] - v.numerator, pos[1] - v.denominator)
                asteroids_set.remove(pos)
                destroyed.append(pos)
                vectors.remove((v, 1))

            # destroy to right if exists
            if cardinal_checks[0]:
                for i in range(x + 1, len(space_map[0])):
                    if (i, y) in asteroids_set:
                        asteroids_set.remove((i, y))
                        destroyed.append((i, y))
                        break

            # go through SE vectors
            current_vectors = [v[0] for v in vectors if v[1] == 1 and v[0] > 0]
            current_vectors.sort(reverse=True)
            for v in current_vectors:
                pos = station_location
                while pos not in asteroids_set:
                    pos = (pos[0] + v.numerator, pos[1] + v.denominator)
                asteroids_set.remove(pos)
                destroyed.append(pos)
                vectors.remove((v, 1))

            # destroy underneath if it exists
            if cardinal_checks[2]:
                for i in range(y + 1, len(space_map)):
                    if (x, i) in asteroids_set:
                        asteroids_set.remove((x,i))
                        destroyed.append((x, i))
                        break

            # go through SW vectors
            current_vectors = [v[0] for v in vectors if v[1] == -1 and v[0] < 0]
            current_vectors.sort(reverse=True)
            for v in current_vectors:
                pos = station_location
                while pos not in asteroids_set:
                    pos = (pos[0] + v.numerator, pos[1] + v.denominator)
                asteroids_set.remove(pos)
                destroyed.append(pos)
                vectors.remove((v, -1))

            # destroy to left if exists
            if cardinal_checks[1]:
                for i in range(x - 1, -1, -1):
                    if (i, y) in asteroids_set:
                        asteroids_set.remove((i, y))
                        destroyed.append((i, y))
                        break

            # go through NW vectors
            current_vectors = [v[0] for v in vectors if v[1] == -1 and v[0] > 0]
            current_vectors.sort(reverse=True)
            for v in current_vectors:
                pos = station_location
                while pos not in asteroids_set:
                    pos = (pos[0] - v.numerator, pos[1] - v.denominator)
                asteroids_set.remove(pos)
                destroyed.append(pos)
                vectors.remove((v, -1))

            if len(asteroids_set) == 0:
                break

        print(destroyed[199][0] * 100 + destroyed[199][1])


solution_part2()
