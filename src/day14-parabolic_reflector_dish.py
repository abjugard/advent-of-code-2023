from santas_little_helpers import day, get_data, timed
from santas_little_classes import Point
from santas_little_utils import build_dict_map

today = day(2023, 14)


def tilt(rocks, the_map, direction='N'):
  rocks = set(rocks)
  cant_move = set()
  last_moved = True

  def locked(rock):
    nr = Point(*rock).next[direction].t
    is_locked = nr not in the_map or the_map[nr] == '#' or nr in cant_move
    if is_locked:
      cant_move.add(rock)
    return is_locked

  def can_move(rock):
    nr = Point(*rock).next[direction].t
    return not locked(rock) and not (nr in rocks or nr in n_rocks)

  def move(rock):
    rock = Point(*rock)
    while can_move(rock.t):
      rock = rock.next[direction]
    return rock.t

  while last_moved:
    last_moved = False
    n_rocks = set()
    for rock in sorted(rocks - cant_move):
      rocks.remove(rock)
      n_rocks.add(move(rock))
      last_moved = True
    n_rocks.update(cant_move)
    rocks = n_rocks
  return tuple(sorted(rocks))


def spin_cycle(the_map, h, rocks):
  c = 0
  seen = dict()

  cycle_found = False
  while c < 1e9:
    for d in 'NWSE':
      rocks = tilt(rocks, the_map, d)
    c += 1
    if not cycle_found:
      if rocks in seen:
        skip = c - seen[rocks]
        c += skip * ((1e9-c) // skip)
        cycle_found = True
      seen[rocks] = c
  return sum(h-y for _, y in rocks)


def init_rocks(the_map):
  rocks = set()
  for p, c in the_map.items():
    if c == 'O':
      rocks.add(p)
  return rocks


def main():
  the_map, (_, h) = build_dict_map(get_data(today))
  rocks = init_rocks(the_map)
  print(f'{today} star 1 = {sum(h-y for _, y in tilt(rocks, the_map, "N"))}')
  print(f'{today} star 2 = {spin_cycle(the_map, h, rocks)}')


if __name__ == '__main__':
  timed(main)
