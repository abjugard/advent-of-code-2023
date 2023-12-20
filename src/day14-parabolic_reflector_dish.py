from santas_little_helpers import day, get_data, timed
from santas_little_classes import Point
from santas_little_utils import build_dict_map, map_frame

today = day(2023, 14)


sorting = {
  'N': lambda p:  p.y,
  'S': lambda p: -p.y,
  'W': lambda p:  p.x,
  'E': lambda p: -p.x,
}


def tilt(rocks, fixed, direction='N'):
  locked = set()
  for rock in sorted(set(rocks), key=sorting[direction]):
    while nr := rock.next(direction):
      if nr in locked or nr in fixed:
        break
      rock = nr
    locked.add(rock)
  return tuple(locked)


def spin_cycle(rocks, fixed, h):
  c = 0
  seen = dict()
  cycle_found = False
  while c < 1e9:
    for d in 'NWSE':
      rocks = tilt(rocks, fixed, d)
    c += 1
    if not cycle_found:
      if rocks in seen:
        skip = c - seen[rocks]
        c += skip * ((1e9-c) // skip)
        cycle_found = True
      seen[rocks] = c
  return sum(h-r.y for r in rocks)


def main():
  the_map, (w, h) = build_dict_map(get_data(today), key_func=lambda c, p: Point(*p))
  rocks, fixed = set(), set(Point(*p) for p in map_frame(w, h))
  for p, c in the_map.items():
    match c:
      case 'O': rocks.add(p)
      case '#': fixed.add(p)
  print(f'{today} star 1 = {sum(h-r.y for r in tilt(rocks, fixed))}')
  print(f'{today} star 2 = {spin_cycle(rocks, fixed, h)}')


if __name__ == '__main__':
  timed(main)
