from santas_little_helpers import day, get_data, timed
from santas_little_classes import Point
from itertools import product

today = day(2023, 11)


def distance_between_galaxies(the_map, expansion):
  assert len(the_map) == len(the_map[0])
  xs, ys = [], []
  size = len(the_map)
  for i in range(size):
    if all(c == '.' for c in the_map[i]):
      ys.append(i)
    if all(c == '.' for row in the_map for c in row[i]):
      xs.append(i)

  galaxies = set()
  for x, y in product(range(size), repeat=2):
    if the_map[y][x] == '#':
      yc = sum(expansion-1 for i in ys if i < y)
      xc = sum(expansion-1 for i in xs if i < x)
      galaxies.add(Point(x+xc, y+yc))

  considered = set()
  distance = 0
  for galaxy in galaxies:
    considered.add(galaxy)
    other_galaxies = galaxies - considered
    for other_galaxy in other_galaxies:
      distance += galaxy.manhattan_distance_to(other_galaxy)
  return distance


def main():
  inp = list(get_data(today))
  print(f'{today} star 1 = {distance_between_galaxies(inp, expansion=2)}')
  print(f'{today} star 2 = {distance_between_galaxies(inp, expansion=1_000_000)}')


if __name__ == '__main__':
  timed(main)
