from santas_little_helpers import day, get_data, timed
from itertools import zip_longest

today = day(2023, 5)


def map_seed(seed, almanac):
  for title, func in almanac.items():
    n_seed = func(seed)
    if n_seed != None:
      seed = n_seed
  return seed


def part1(seeds, almanac):
  locations = []
  for seed in seeds:
    location = map_seed(seed, almanac)
    locations.append(location)
  return min(locations)


def grouper(iterable, n, fillvalue=None):
  args = [iter(iterable)] * n
  return zip_longest(fillvalue=fillvalue, *args)


def part2(seeds, almanac):
  locations = []
  for seed_start, r_len in grouper(seeds, 2):
    for seed in range(seed_start, seed_start+r_len):
      locations.append(map_seed(seed, almanac))
    print(min(locations))
  return min(locations)


def mapping_fn(table):
  def conv_func(n):
    for dst_start, src_start, r_len in table:
      if n in range(src_start, src_start+r_len):
        return n-src_start+dst_start
    return None
  return conv_func


def parse(groups):
  almanac = dict()
  for group in groups:
    title, *lines = group
    title = title[:-5]
    table = []
    for l in lines:
      table.append(list(map(int, l.split())))
    almanac[title] = mapping_fn(table)
  return almanac


def main():
  seeds, *inp = list(get_data(today, groups=True))
  seeds = list(map(int, next(seeds).split(':')[1].split()))
  almanac = parse(inp)
  print(f'{today} star 1 = {part1(seeds, almanac)}')
  print(f'{today} star 2 = {part2(seeds, almanac)}')


if __name__ == '__main__':
  timed(main)
