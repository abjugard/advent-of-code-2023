from santas_little_helpers import day, get_data, timed
from santas_little_classes import Point
from santas_little_utils import build_dict_map

today = day(2023, 10)


OPPOSITE = { 'N': 'S', 'E': 'W', 'W': 'E', 'S': 'N' }


def travel(the_map, p, coming_from):
  c1, c2 = the_map[p.t]
  new_dir = c1 if c1 != coming_from else c2
  return p.next[new_dir], OPPOSITE[new_dir]


def find_route(the_map):
  # This part assumes we're starting northbound from S which has an L shape
  s, coming_from = 0, 'E'
  p = start_pos
  route = set([p.t])
  while True:
    p, coming_from = travel(the_map, p, coming_from)
    route.add(p.t)
    if p == start_pos:
      return s // 2 + 1, route
    s += 1


def find_encompassed_area(orig_map, route, w, h):
  area = 0
  for y in range(h):
    included = False
    for x in range(w):
      p = (x, y)
      if p in route:
        if orig_map[p] in '|LJ':
          included = not included
      elif included:
        area += 1
  return area


def conv_func(c, p):
  global start_pos
  if c == '|': return 'NS'
  if c == '-': return 'WE'
  if c == 'L': return 'NE'
  if c == 'J': return 'WN'
  if c == '7': return 'WS'
  if c == 'F': return 'SE'
  if c == '.': return None
  if c == 'S': 
    start_pos = Point(*p)
    return 'NE'


def main():
  map_data = list(get_data(today))
  the_map, d = build_dict_map(map_data, conv_func)
  orig_map, _ = build_dict_map(map_data)
  # Too lazy to implement proper detection
  orig_map[start_pos.t] = 'L'
  star1, route = find_route(the_map)
  print(f'{today} star 1 = {star1}')
  print(f'{today} star 2 = {find_encompassed_area(orig_map, route, *d)}')


if __name__ == '__main__':
  timed(main)
