def solution_part1(fname):
    with open(fname, "r") as f:
        parents = {}
        for line in f:
            [parent, child] = line[:-1].split(")")
            parents[child] = parent
        print(sum([solve(x, parents) for x in parents]))


solved = {
    "COM": 0
}

def solve(current, parents):
    if current in solved:
        return solved[current]
    result = 1 + solve(parents[current], parents)
    solved[current] = result
    return result

class Node:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.children = []
        self.you_distance = 9999999999
        self.san_distance = 9999999999

    def __repr__(self):
        return self.name


def solution_part2(fname):
    with open(fname, "r") as f:
        nodes = {}
        for line in f:
            [parent, child] = line[:-1].split(")")
            if parent not in nodes:
                nodes[parent] = Node(parent, None)
            parent_node = nodes[parent]
            nodes[child] = Node(child, parent)
            parent_node.children.append(child)

        current = "SAN"
        nodes[current].san_distance = 0
        while nodes[current].parent != None:
            nodes[nodes[current].parent].san_distance = nodes[current].san_distance + 1
            current = nodes[current].parent

        current = "YOU"
        nodes[current].you_distance = 0
        while nodes[current].parent != None:
            nodes[nodes[current].parent].you_distance = nodes[current].you_distance + 1
            current = nodes[current].parent

        print(min([n.san_distance + n.you_distance for n in nodes.values()]) - 2)

solution_part2("inputs/day6.txt")
