from santas_little_helpers import day, get_data, timed
from santas_little_utils import build_dict_map, directions_4
import numpy as np

today = day(2023, 21)


def neighbours(x, y):
  for _, (xd, yd) in directions_4:
    xn, yn = x + xd, y + yd
    if (xn % w, yn % h) in the_map:
      yield (xn, yn)


def bfs(steps):
  seen, ps = set(), set([start])
  for _ in range(steps):
    new_ps = set()
    for p in ps:
      new_ps.update(neighbours(*p))
    seen.update(ps)
    ps = new_ps - seen
  seen.update(ps)
  return sum(1 for p in seen if sum(p) % 2 == steps % 2)


def extrapolate_reachable():
  ys = [bfs(steps) for steps in [65, 65 + 131, 65 + 131 * 2]]
  xs = [0, 1, 2]
  coefficients = np.polyfit(xs, ys, 2)
  result = np.polyval(coefficients, (26501365 - 65) // 131)
  return int(np.round(result))


def main():
  global the_map, start, w, h
  the_map, (w, h) = build_dict_map(get_data(today))
  for p, c in the_map.copy().items():
    if c == 'S':
      start = p
    if c == '#':
      del the_map[p]
  the_map = set(the_map.keys())
  print(f'{today} star 1 = {bfs(steps=64)}')
  print(f'{today} star 2 = {extrapolate_reachable()}')


if __name__ == '__main__':
  timed(main)
