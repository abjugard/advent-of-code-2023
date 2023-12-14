from santas_little_helpers import day, get_data, timed
from santas_little_classes import Point
from santas_little_utils import build_dict_map

today = day(2023, 10)


OPPOSITE = { 'N': 'S', 'E': 'W', 'W': 'E', 'S': 'N' }
SHAPE_MAPPER = { '|': 'NS','-': 'WE','L': 'NE','J': 'WN','7': 'WS','F': 'SE' }


def travel(the_map, p, coming_from):
  c1, c2 = the_map[p.t]
  new_dir = c1 if c1 != coming_from else c2
  return p.next(new_dir), OPPOSITE[new_dir]


def find_route(the_map):
  first_possible, _ = the_map[start_pos.t]
  s, coming_from = 0, OPPOSITE[first_possible]
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
  if c in SHAPE_MAPPER:
    return SHAPE_MAPPER[c]
  if c == 'S':
    start_pos = Point(*p)
  return None


def determine_start_shape(the_map):
  exits = []
  for d in 'NEWS':
    n = start_pos.next(d)
    n_possibles = the_map[n.t]
    if OPPOSITE[d] in n_possibles:
      exits.append(d)
  for shape, possibles in SHAPE_MAPPER.items():
    if all(e in possibles for e in exits):
      return shape


def main():
  map_data = list(get_data(today))
  the_map, d = build_dict_map(map_data, conv_func)
  shape = determine_start_shape(the_map)
  the_map[start_pos.t] = SHAPE_MAPPER[shape]
  orig_map, _ = build_dict_map(map_data)
  orig_map[start_pos.t] = shape
  star1, route = find_route(the_map)
  print(f'{today} star 1 = {star1}')
  print(f'{today} star 2 = {find_encompassed_area(orig_map, route, *d)}')


if __name__ == '__main__':
  timed(main)
