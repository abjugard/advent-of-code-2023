from santas_little_helpers import day, get_data, timed
from collections import defaultdict

today = day(2023, 4)


def find_matches(winning, have):
  m = 0
  for n in have:
    if n in winning:
      m += 1
  return m


def scratchcard_points(inp):
  s = 0
  lookup = dict()
  for idx, winning, have in inp:
    matches = find_matches(winning, have)
    lookup[idx] = matches
    if matches > 0:
      v = 1
      for _ in range(matches - 1):
        v *= 2
      s += v
  return s, lookup


def scratchcards_won(lookup):
  copies = defaultdict(int)
  for idx, matches in lookup.items():
    copies[idx] += 1
    n = copies[idx]
    for i in range(idx+1, idx+matches+1):
      copies[i] += n
  return sum(copies.values())


def parse(line):
  idx, rest = line.split(': ')
  idx = int(idx[4:].strip())
  winning, have = rest.split(' | ')
  winning = list(map(int, winning.strip().replace('  ', ' ').split(' ')))
  have = list(map(int, have.strip().replace('  ', ' ').split(' ')))
  return (idx, winning, have)


def main():
  inp = list(get_data(today, [('func', parse)]))
  star1, lookup = scratchcard_points(inp)
  print(f'{today} star 1 = {star1}')
  print(f'{today} star 2 = {scratchcards_won(lookup)}')


if __name__ == '__main__':
  timed(main)
