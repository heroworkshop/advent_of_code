import re

W, H, i, data = 101, 103, 0, [list(map(int, re.search('p=(\d+),(\d+) v=(-*\d+),(-*\d+)', line).groups())) for line in open('14.txt')]
f = lambda s: [((px + s * vx) % W, (py + s * vy) % H) for px, py, vx, vy in data]
print(eval('*'.join([str(len([(x, y) for (x, y) in f(100) if a * (x - W // 2) > 0 and b * (y - H // 2) > 0])) for a in [1, -1] for b in [1, -1]])))
while len(set(f(i := i + 1))) != len(data): pass
print(i)

