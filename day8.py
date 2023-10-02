def solution_part1(fname="inputs/day8.txt"):
    with open(fname, "r") as f:
        image_width = 25
        image_height = 6

        pixels = [int(x) for x in f.readline()[:-1]]
        min_0_digits = 99999999999
        result = 0
        i = 0
        while i < len(pixels):
            counts = [0, 0, 0]
            for _ in range(image_width * image_height):
                counts[pixels[i]] += 1
                i += 1
            if counts[0] < min_0_digits:
                min_0_digits = counts[0]
                result = counts[1] * counts[2]

        print(result)
        return result


def solution_part2(fname="inputs/day8.txt"):
    with open(fname, "r") as f:
        image_width = 25
        image_height = 6

        image = [[2 for _ in range(image_width)] for _ in range(image_height)]
        pixels = [int(x) for x in f.readline()[:-1]]
        i = 0
        while i < len(pixels):
            j = i % (image_width * image_height)
            r = int(j / image_width)
            c = j % image_width

            if image[r][c] == 2:
                image[r][c] = pixels[i]

            i += 1

        for x in image:
            print("".join(["O" if c == 1 else "." for c in x]))

solution_part2()
