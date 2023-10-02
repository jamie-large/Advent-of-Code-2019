import math

def solution_part1(fname="inputs/day14.txt"):
    with open(fname, "r") as f:
        recipes = {}
        for line in f:
            inputs, output = line.split("=>")
            output = output.split()
            inputs = [x.split() for x in inputs.split(",")]
            inputs = [(int(x[0]), x[1]) for x in inputs]
            recipes[output[1]] = (int(output[0]), inputs)

        constructed_being_used = {}
        constructed = {}
        constructing = {
            "FUEL": 1
        }

        while len(constructing) > 1 or "ORE" not in constructing:
            for m in list(constructing.keys()):
                if m == "ORE":
                    continue
                amount_needed = constructing.pop(m)
                recipe = recipes[m]

                amount_on_hand = constructed.get(m, 0) - constructed_being_used.get(m, 0)

                amount_to_make = amount_needed - amount_on_hand

                # If we need to, construct additional batches
                if amount_to_make > 0:
                    batches_to_make = math.ceil(amount_to_make / recipe[0])
                    constructed[m] = constructed.get(m, 0) + batches_to_make * recipe[0]
                    for comp in recipe[1]:
                        constructing[comp[1]] = constructing.get(comp[1], 0) + comp[0] * batches_to_make

                # Update how much we're using
                constructed_being_used[m] = constructed_being_used.get(m, 0) + amount_needed

        print(constructing["ORE"])
        return constructing["ORE"], recipes

def solution_part2(fname="inputs/day14.txt"):
    min_ore, recipes = solution_part1(fname)

    ITER = 100000

    fuel_level = int(1000000000000 / min_ore)

    while ITER > 0:
        constructed_being_used = {}
        constructed = {}
        constructing = {
            "FUEL": fuel_level,
            "ORE": 0
        }

        fuel_made = constructing["FUEL"]
        while constructing["ORE"] < 1000000000000:
            constructing["FUEL"] = constructing.get("FUEL", 0) + ITER
            while len(constructing) > 1:
                for m in list(constructing.keys()):
                    if m == "ORE":
                        continue
                    amount_needed = constructing.pop(m)
                    recipe = recipes[m]

                    amount_on_hand = constructed.get(m, 0) - constructed_being_used.get(m, 0)

                    amount_to_make = amount_needed - amount_on_hand

                    # If we need to, construct additional batches
                    if amount_to_make > 0:
                        batches_to_make = math.ceil(amount_to_make / recipe[0])
                        constructed[m] = constructed.get(m, 0) + batches_to_make * recipe[0]
                        for comp in recipe[1]:
                            constructing[comp[1]] = constructing.get(comp[1], 0) + comp[0] * batches_to_make

                    # Update how much we're using
                    constructed_being_used[m] = constructed_being_used.get(m, 0) + amount_needed
            fuel_made += ITER

        fuel_level = fuel_made - ITER
        ITER = int(ITER / 10)

    print(fuel_level)

solution_part2()

