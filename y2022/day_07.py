from collections import defaultdict

from aocd_tools import load_input_data

EXAMPLE = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""


class Folder(dict):
    def add_subdir(self, name):
        self[name] = Folder()

    def add_file(self, name, size):
        self[name] = size

    def size(self):
        total = 0
        for _, f in self.items():
            size = f.size() if hasattr(f, "size") else f
            total += size
        return total


def find_sizes(folder):
    sizes = [folder.size()]
    for _, f in folder.items():
        if isinstance(f, Folder):
            sizes.extend(find_sizes(f))
    return sizes


def run():
    input_data = load_input_data(2022, 7)
    # input_data = EXAMPLE

    print(f"loaded input data ({len(input_data)} bytes)")

    root = parse(input_data)

    print("solution1 = ", solution1(root))
    print("solution2 = ", solution2(root))


def parse(input_data):
    root = Folder()
    path = []
    lines = input_data.split("\n")
    for line in lines:
        print(line)
        if line == "$ cd /":
            path = []
        elif line == "$ cd ..":
            path.pop()
        elif line.startswith("$ cd "):
            cd_to = line.split()[-1]
            path.append(cd_to)
        elif line == "$ ls":
            pass
        else:
            metadata, name = line.split()
            create(name, metadata, path, root)
        print(f"{path}>")

    return root


def create(name, metadata, path, root):
    p = root
    for d in path:
        p = p[d]
    if metadata == "dir":
        p.add_subdir(name)
    else:
        p.add_file(name, int(metadata))


def solution1(root):
    sizes = find_sizes(root)
    return sum(s for s in sizes if s <=100000)


def solution2(root):
    required = 70000000
    free = required - root.size()
    extra = 30000000 - free
    sizes = find_sizes(root)
    sizes.sort()
    print(sizes)
    for s in sizes:
        if s >= extra:
            return s


if __name__ == "__main__":
    run()
