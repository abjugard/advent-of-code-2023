from santas_little_helpers import day, get_data, timed
from santas_little_classes import Point
from santas_little_utils import build_dict_map, map_frame

today = day(2023, 14)


def tilt(rocks, fixed, direction='N'):
  loose = set(rocks)
  locked = set()
  while loose:
    for rock in loose.copy():
      loose.remove(rock)
      while nr := rock.next(direction):
        is_locked = nr in locked or nr in fixed
        if is_locked or nr in loose:
          break
        rock = nr
      (locked if is_locked else loose).add(rock)
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
