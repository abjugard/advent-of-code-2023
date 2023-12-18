from santas_little_helpers import day, get_data, timed
from santas_little_utils import build_dict_map, neighbours
import heapq

today = day(2023, 17)

OPPOSITE = { 'N': 'S', 'E': 'W', 'W': 'E', 'S': 'N' }


def minimum_heat_loss(the_map, w, h, ultra_crucible=False):
  to_check = [(0, (0, 0), None, None)]
  seen = set()
  path_costs = []
  while to_check:
    s, p, direction, in_direction = heapq.heappop(to_check)
    if (p, direction, in_direction) in seen:
      continue
    seen.add((p, direction, in_direction))
    for new_direction, np in neighbours(p, the_map, labels=True):
      new_in_direction = in_direction + 1 if new_direction == direction else 1
      if not direction is None:
        if new_direction == OPPOSITE[direction]:
          continue
        if new_in_direction > (10 if ultra_crucible else 3):
          continue
        if ultra_crucible:
          if new_direction != direction and in_direction < 4:
            continue
      cost = s + the_map[np]
      if np == (w-1, h-1):
        if not ultra_crucible or new_in_direction >= 4:
          path_costs.append(cost)
      heapq.heappush(to_check, (cost, np, new_direction, new_in_direction))
  return min(path_costs)


def main():
  the_map, (w, h) = build_dict_map(get_data(today), conv_func=lambda c, p: int(c))
  print(f'{today} star 1 = {minimum_heat_loss(the_map, w, h)}')
  print(f'{today} star 2 = {minimum_heat_loss(the_map, w, h, ultra_crucible=True)}')


if __name__ == '__main__':
  timed(main)
