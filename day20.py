def solution_part1(fname="inputs/day20.txt"):
    with open(fname, "r") as f:
        maze = [[x for x in line[:-1]] for line in f.readlines()]

        portals = find_portals(maze)

        start_position: tuple = portals.pop("AA")[0]
        end_position: tuple = portals.pop("ZZ")[0]

        queue = [(start_position, 0)]
        visited = set()
        processing = set([start_position])

        while len(queue) > 0:
            current_position, steps = queue.pop(0)
            visited.add(current_position)
            processing.remove(current_position)

            if current_position == end_position:
                print(steps)
                return

            neighbors = [(current_position[0]-1, current_position[1]), (current_position[0]+1, current_position[1]),
                         (current_position[0], current_position[1]-1), (current_position[0], current_position[1]+1)]
            next_positions = []
            for (i, j) in neighbors:
                if maze[i][j] == "." and (i, j) not in visited and (i, j) not in processing:
                    next_positions.append((i, j))
                elif maze[i][j].isalpha():
                    portal_name = maze[i-1][j] + maze[i][j] if i < current_position[0] else \
                                  maze[i][j] + maze[i+1][j] if i > current_position[0] else \
                                  maze[i][j-1] + maze[i][j] if j < current_position[1] else \
                                  maze[i][j] + maze[i][j+1]
                    if portal_name == "AA":
                        continue
                    portal_positions = portals[portal_name]
                    np = (portal_positions[0] if current_position == portal_positions[1] else portal_positions[1])
                    if np not in visited and np not in processing:
                        next_positions.append(np)

            for np in next_positions:
                queue.append((np, steps + 1))
                processing.add(np)


def find_portals(maze: list[list[str]]):
    portals = {}
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j].isalpha():
                if i + 1 < len(maze) and j < len(maze[i+1]) and maze[i+1][j].isalpha():
                    portal_name = maze[i][j] + maze[i+1][j]
                    portal_position = (i+2, j) if i + 2 < len(maze) and maze[i+2][j] == "." else (i-1, j)
                    current = portals.get(portal_name, [])
                    current.append(portal_position)
                    portals[portal_name] = current
                elif j + 1 < len(maze[i]) and maze[i][j+1].isalpha():
                    portal_name = maze[i][j] + maze[i][j+1]
                    portal_position = (i, j+2) if j + 2 < len(maze[i]) and maze[i][j+2] == "." else (i, j-1)
                    current = portals.get(portal_name, [])
                    current.append(portal_position)
                    portals[portal_name] = current
    return portals

def solution_part2(fname="inputs/day20.txt"):
    with open(fname, "r") as f:
        maze = [[x for x in line[:-1]] for line in f.readlines()]

        portals = find_portals(maze)

        start_position: tuple = portals.pop("AA")[0]
        end_position: tuple = portals.pop("ZZ")[0]

        start_position = (start_position[0], start_position[1], 0)
        end_position = (end_position[0], end_position[1], 0)

        queue = [(start_position, 0)]
        visited = set()
        processing = set([start_position])

        while len(queue) > 0:
            # print(queue)
            current_position, steps = queue.pop(0)
            visited.add(current_position)
            processing.remove(current_position)

            if current_position == end_position:
                print(steps)
                return

            neighbors = [(current_position[0]-1, current_position[1]), (current_position[0]+1, current_position[1]),
                         (current_position[0], current_position[1]-1), (current_position[0], current_position[1]+1)]
            next_positions = []
            for (i, j) in neighbors:
                if maze[i][j] == "." and (i, j, current_position[2]) not in visited and (i, j, current_position[2]) not in processing:
                    next_positions.append((i, j, current_position[2]))
                elif maze[i][j].isalpha():
                    portal_name = maze[i-1][j] + maze[i][j] if i < current_position[0] else \
                                  maze[i][j] + maze[i+1][j] if i > current_position[0] else \
                                  maze[i][j-1] + maze[i][j] if j < current_position[1] else \
                                  maze[i][j] + maze[i][j+1]
                    if portal_name == "AA" or portal_name == "ZZ":
                        continue

                    outer = i in (0, 1, len(maze) - 1, len(maze) - 2) or j in (0, 1, len(maze[i]) - 1, len(maze[i]) - 2)

                    if outer and current_position[2] == 0:
                        continue

                    portal_positions = portals[portal_name]
                    np = (portal_positions[0] if current_position[0] == portal_positions[1][0] and current_position[1] == portal_positions[1][1] else portal_positions[1])

                    np = (np[0], np[1], current_position[2] + (-1 if outer else 1))

                    if np not in visited and np not in processing:
                        next_positions.append(np)

            for np in next_positions:
                queue.append((np, steps + 1))
                processing.add(np)
        print("COULD NOT FIND")

solution_part2()
