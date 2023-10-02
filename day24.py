def solution_part1(fname="inputs/day24.txt"):
    with open(fname, "r") as f:
        grid = ""
        for line in f:
            grid += line[:-1]

        seen_grids: set[str] = set()
        seen_grids.add(grid)

        while True:
            grid = get_next_grid(grid)
            if grid in seen_grids:
                result = 0
                for i in range(len(grid)):
                    if grid[i] == "#":
                        result += 2 ** i
                print(result)
                return
            seen_grids.add(grid)

def get_next_grid(grid: str):
    new_grid = []
    for i in range(len(grid)):
        neighboring_bugs = 0
        if i + 5 < len(grid) and grid[i+5] == "#":
            neighboring_bugs += 1
        if i - 5 >= 0 and grid[i-5] == "#":
            neighboring_bugs += 1

        if i % 5 != 4 and grid[i+1] == "#":
            neighboring_bugs += 1
        if i % 5 != 0 and grid[i-1] == "#":
            neighboring_bugs += 1

        if grid[i] == "#" and neighboring_bugs != 1:
            new_grid.append(".")
        elif grid[i] == "." and (neighboring_bugs == 1 or neighboring_bugs == 2):
            new_grid.append("#")
        else:
            new_grid.append(grid[i])

    return "".join(new_grid)

EMPTY_GRID = "............?............"

def solution_part2(fname="inputs/day24.txt"):
    with open(fname, "r") as f:
        grids: dict[int, str] = dict()
        grids[0] = ""
        for line in f:
            grids[0] += line[:-1]

        grids[-1] = EMPTY_GRID
        grids[1] = EMPTY_GRID

        for _ in range(200):
            new_grids = dict()
            min_g = 10000
            max_g = -10000
            for g in grids:
                if g < min_g:
                    min_g = g
                if g > max_g:
                    max_g = g
                new_grid = []
                grid = grids[g]
                for i in range(25):
                    neighboring_bugs = 0
                    # Count neighbors below
                    if i + 5 == 12:
                        if g + 1 in grids:
                            neighboring_bugs += sum([1 for x in grids[g+1][:5] if x == "#"])
                    elif i + 5 >= len(grid):
                        if g - 1 in grids and grids[g-1][17] == "#":
                            neighboring_bugs += 1
                    elif grid[i+5] == "#":
                        neighboring_bugs += 1

                    # Count neighbors above
                    if i - 5 == 12:
                        if g + 1 in grids:
                            neighboring_bugs += sum([1 for x in grids[g+1][20:] if x == "#"])
                    elif i - 5 < 0:
                        if g - 1 in grids and grids[g-1][7] == "#":
                            neighboring_bugs += 1
                    elif grid[i-5] == "#":
                        neighboring_bugs += 1

                    # Count neighbors to right
                    if i + 1 == 12:
                        if g + 1 in grids:
                            neighboring_bugs += sum([1 for x in grids[g+1][0:25:5] if x == "#"])
                    elif i % 5 == 4:
                        if g - 1 in grids and grids[g-1][13] == "#":
                            neighboring_bugs += 1
                    elif grid[i+1] == "#":
                        neighboring_bugs += 1

                    # Count neighbors to left
                    if i - 1 == 12:
                        if g + 1 in grids:
                            neighboring_bugs +=sum([1 for x in grids[g+1][4:25:5] if x == "#"])
                    elif i % 5 == 0:
                        if g - 1 in grids and grids[g-1][11] == "#":
                            neighboring_bugs += 1
                    elif grid[i-1] == "#":
                        neighboring_bugs += 1

                    if grid[i] == "#" and neighboring_bugs != 1:
                        new_grid.append(".")
                    elif grid[i] == "." and (neighboring_bugs == 1 or neighboring_bugs == 2):
                        new_grid.append("#")
                    else:
                        new_grid.append(grid[i])
                new_grids[g] = "".join(new_grid)

            if grids[min_g] != EMPTY_GRID:
                new_grids[min_g - 1] = EMPTY_GRID
            if grids[max_g] != EMPTY_GRID:
                new_grids[max_g + 1] = EMPTY_GRID

            grids = new_grids

        result = sum([sum([1 for x in grids[g] if x == "#"]) for g in grids])

        print(result)

solution_part2()
