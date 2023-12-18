from santas_little_helpers import day, get_data, timed
from santas_little_classes import Origo as O
from itertools import pairwise

today = day(2023, 18)

DIRECTION = { 'D': O.s, 'L': O.w, 'R': O.e, 'U': O.n }
H_DIRECTION = { '0': O.e, '1': O.s, '2': O.w, '3': O.n }


def shoelace_area(ps):
  area = 0
  for p, p_n in pairwise(ps):
    area += p.x * p_n.y - p_n.x * p.y
  return abs(area) // 2


def lagoon_volume(dig_plan):
  digger = O.copy
  perimeter = 0
  ps = []
  for direction, s in dig_plan:
    ps.append(digger.move(direction, s).copy)
    perimeter += s
  ps.append(ps[0])
  return int(shoelace_area(ps) + perimeter // 2 + 1)


def parse(line):
  d, l, h = line.split()
  l = DIRECTION[d], int(l)
  r = H_DIRECTION[h[-2]], int(h[2:-2], 16)
  return l, r


def main():
  dig_plan = list(get_data(today, [('func', parse)]))
  l_plan, r_plan = zip(*dig_plan)
  print(f'{today} star 1 = {lagoon_volume(l_plan)}')
  print(f'{today} star 2 = {lagoon_volume(r_plan)}')


if __name__ == '__main__':
  timed(main)
