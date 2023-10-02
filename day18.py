def solution_part1(fname="inputs/day18.txt"):
    with open(fname, "r") as f:
        room = [[x for x in line[:-1]] for line in f.readlines()]

        starting_position = (0, 0)

        key_locations = {}
        door_locations = {}
        for i in range(len(room)):
            for j in range(len(room[i])):
                symbol = room[i][j]
                if symbol.islower():
                    key_locations[symbol] = (i, j)
                elif symbol.isupper():
                    door_locations[symbol] = (i, j)
                elif symbol == "@":
                    starting_position = (i, j)

        all_keys = list(key_locations.keys())

        key_distances = {}

        for i in range(len(all_keys)):
            for j in range(i+1, len(all_keys)):
                dist = calculate_distance_and_blockers(room, key_locations[all_keys[i]], key_locations[all_keys[j]])
                key_distances[(all_keys[i], all_keys[j])] = dist
                key_distances[(all_keys[j], all_keys[i])] = dist
            key_distances[("@", all_keys[i])] = calculate_distance_and_blockers(room, starting_position, key_locations[all_keys[i]])

        possible_routes = [(["@"], 0, set(["@"]))]
        keep_going = True

        while keep_going:
            keep_going = False
            new_routes = []

            for found_keys, steps, found_keys_set in possible_routes:
                unlocked_doors_set = set([x.upper() for x in found_keys])
                for next_key in all_keys:
                    # Make sure we don't have the key yet
                    if next_key in found_keys_set:
                        continue
                    next_key_distance, next_key_blockers = key_distances[found_keys[-1], next_key]
                    # Make sure key isn't blocked
                    for blocker in next_key_blockers:
                        if blocker not in found_keys_set and blocker not in unlocked_doors_set:
                            break
                    else:
                        new_keys = found_keys + [next_key]
                        new_steps = steps + next_key_distance
                        new_keys_set = set(new_keys)

                        # Make sure we only have 1 route at this position with these keys
                        for i in range(len(new_routes)):
                            nr = new_routes[i]
                            if nr[0][-1] == next_key and nr[2] == new_keys_set:
                                if new_steps < nr[1]:
                                    new_routes[i] = ((new_keys, new_steps, new_keys_set))
                                break
                        else:
                            new_routes.append((new_keys, new_steps, new_keys_set))
                            if len(new_routes[-1][0]) < len(all_keys) + 1:
                                keep_going = True

            possible_routes = new_routes
            print(f"Found {len(possible_routes[0][2]) - 1} / {len(all_keys)} keys")

        result = min(possible_routes, key=lambda x: x[1])[1]
        print(result)


def calculate_distance_and_blockers(room, start, end):
    queue = [(start, 0)]
    previous = { start: None }

    while len(queue) > 0:
        position, steps = queue.pop(0)

        # If we've found the end, return
        if position == end:
            blockers = set()
            current = previous[position]

            # Figure out blockers
            while current != start:
                if room[current[0]][current[1]].isupper() or room[current[0]][current[1]].islower():
                    blockers.add(room[current[0]][current[1]])

                current = previous[current]

            return steps, blockers

        # Otherwise, add neigbors
        neighbors = [(position[0] + 1, position[1]), (position[0] - 1, position[1]), (position[0], position[1] + 1), (position[0], position[1] - 1)]
        for n in neighbors:
            if n not in previous and room[n[0]][n[1]] != "#":
                previous[n] = position
                queue.append((n, steps + 1))

def solution_part2(fname="inputs/day18.txt"):
    with open(fname, "r") as f:
        room = [[x for x in line[:-1]] for line in f.readlines()]

        starting_position = (0, 0)

        key_locations = {}
        door_locations = {}
        for i in range(len(room)):
            for j in range(len(room[i])):
                symbol = room[i][j]
                if symbol.islower():
                    key_locations[symbol] = (i, j)
                elif symbol.isupper():
                    door_locations[symbol] = (i, j)
                elif symbol == "@":
                    starting_position = (i, j)

        location_keys = {}
        for k in key_locations:
            location_keys[key_locations[k]] = k

        room[starting_position[0] - 1][starting_position[1] - 1] = "0"
        room[starting_position[0] - 1][starting_position[1]] = "#"
        room[starting_position[0] - 1][starting_position[1] + 1] = "1"
        room[starting_position[0]][starting_position[1] - 1] = "#"
        room[starting_position[0]][starting_position[1]] = "#"
        room[starting_position[0]][starting_position[1] + 1] = "#"
        room[starting_position[0] + 1][starting_position[1] - 1] = "2"
        room[starting_position[0] + 1][starting_position[1]] = "#"
        room[starting_position[0] + 1][starting_position[1] + 1] = "3"

        starting_positions = [(starting_position[0] - 1, starting_position[1] - 1), \
                              (starting_position[0] - 1, starting_position[1] + 1), \
                              (starting_position[0] + 1, starting_position[1] - 1), \
                              (starting_position[0] + 1, starting_position[1] + 1)]

        all_keys = list(key_locations.keys())

        key_distances = {}

        for i in range(len(all_keys)):
            for j in range(i+1, len(all_keys)):
                dist = calculate_distance_and_blockers(room, key_locations[all_keys[i]], key_locations[all_keys[j]])
                if dist:
                    key_distances[(all_keys[i], all_keys[j])] = dist
                    key_distances[(all_keys[j], all_keys[i])] = dist
            for robot_num in [0, 1, 2, 3]:
                dist = calculate_distance_and_blockers(room, starting_positions[robot_num], key_locations[all_keys[i]])
                if dist:
                    key_distances[(str(robot_num), all_keys[i])] = dist

        # robot_positions, found keys, steps
        possible_routes = [(starting_positions, 0, set())]
        keep_going = True

        while keep_going:
            keep_going = False
            new_routes = []

            for robot_positions, steps, found_keys_set in possible_routes:
                unlocked_doors_set = set([x.upper() for x in found_keys_set])
                for next_key in all_keys:
                    # Make sure we don't have the key yet
                    if next_key in found_keys_set:
                        continue

                    # Figure out which robot can get this key
                    valid_robot_number = [x for x in ["0", "1", "2", "3"] if (x, next_key) in key_distances][0]
                    valid_robot_position = robot_positions[int(valid_robot_number)]
                    valid_robot_symbol = location_keys[valid_robot_position] if valid_robot_position in location_keys else valid_robot_number

                    next_key_distance, next_key_blockers = key_distances[(valid_robot_symbol, next_key)]
                    # Make sure key isn't blocked
                    for blocker in next_key_blockers:
                        if blocker not in found_keys_set and blocker not in unlocked_doors_set:
                            break
                    else:
                        new_robot_positions = [x for x in robot_positions]
                        new_robot_positions[int(valid_robot_number)] = key_locations[next_key]
                        new_steps = steps + next_key_distance
                        new_keys_set = set(list(found_keys_set) + [next_key])

                        # Make sure we only have 1 route at these positions with these keys
                        for i in range(len(new_routes)):
                            nr = new_routes[i]
                            if nr[0] == new_robot_positions and nr[2] == new_keys_set:
                                if new_steps < nr[1]:
                                    new_routes[i] = ((new_robot_positions, new_steps, new_keys_set))
                                break
                        else:
                            new_routes.append((new_robot_positions, new_steps, new_keys_set))
                            if len(new_routes[0][2]) < len(all_keys):
                                keep_going = True

            possible_routes = new_routes
            print(f"Found {len(possible_routes[0][2])} / {len(all_keys)} keys")

        result = min(possible_routes, key=lambda x: x[1])[1]
        print(result)

solution_part2()
