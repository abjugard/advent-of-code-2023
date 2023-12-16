from santas_little_helpers import day, get_data, timed
from santas_little_classes import Point
from santas_little_utils import build_dict_map

today = day(2023, 16)


rot = {
  'E': {'/': 'N', '\\': 'S'},
  'W': {'/': 'S', '\\': 'N'},
  'N': {'/': 'E', '\\': 'W'},
  'S': {'/': 'W', '\\': 'E'}
}


def energized(the_map, init=((0, 0), 'E')):
  traveled = set()
  seen = set()
  beams = [init]
  while beams:
    pos, d = beams.pop()
    while pos in the_map and (pos, d) not in seen:
      traveled.add(pos)
      seen.add((pos, d))
      c = the_map[pos]
      if c in '\\/':
        d = rot[d][the_map[pos]]
      p = Point(*pos)
      if (d in 'EW' and c == '|') or (d in 'NS' and c == '-'):
        for dn in rot[d].values():
          beams.append((p.next(dn).t, dn))
        break
      pos = p.next(d).t
  return len(traveled)


def max_energized(the_map, w, h):
  q = []
  for x in range(w):
    q.append(((x, 0), 'S'))
    q.append(((x, h-1), 'N'))
  for y in range(h):
    q.append(((0, y), 'E'))
    q.append(((w-1, y), 'W'))
  return max(energized(the_map, init) for init in q)


def main():
  the_map, dimensions = build_dict_map(get_data(today))
  print(f'{today} star 1 = {energized(the_map)}')
  print(f'{today} star 2 = {max_energized(the_map, *dimensions)}')


if __name__ == '__main__':
  timed(main)
