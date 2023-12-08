from santas_little_helpers import day, get_data, timed
from math import lcm

today = day(2023, 8)


def steps_to_target(steps, the_map, pos='AAA', criteria='ZZZ'):
  s = 0
  while not pos.endswith(criteria):
    for c in steps:
      pos = the_map[pos][c]
      s += 1
  return s


def ghost_movements(steps, the_map):
  starts = [p for p in the_map if p.endswith('A')]
  ns = []
  for p in starts:
    ns.append(steps_to_target(steps, the_map, pos=p, criteria='Z'))
  return lcm(*ns)


def parse_map(lines):
  the_map = dict()
  for line in lines:
    p, t = line.split(' = ')
    l, r = t[1:-1].split(', ')
    the_map[p] = {'L': l, 'R': r}
  return the_map


def main():
  steps, the_map = get_data(today, groups=True)
  steps, the_map = next(steps), parse_map(the_map)
  print(f'{today} star 1 = {steps_to_target(steps, the_map)}')
  print(f'{today} star 2 = {ghost_movements(steps, the_map)}')


if __name__ == '__main__':
  timed(main)
