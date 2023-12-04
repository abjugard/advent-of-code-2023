from santas_little_helpers import day, get_data, timed
from collections import defaultdict

today = day(2023, 4)


def scratchcards_won(lookup):
  copies = defaultdict(int)
  for idx, matches in lookup.items():
    copies[idx] += 1
    for i in range(idx+1, idx+matches+1):
      copies[i] += copies[idx]
  return sum(copies.values())


def score(match_count):
  v = 1 if match_count else 0
  for _ in range(match_count - 1):
    v *= 2
  return v


def scratchcard_matches(cards):
  return {idx: len(have & winning) for idx, winning, have in cards}


def parse(line):
  idx, rest = line.split(':')
  idx = int(idx[4:].strip())
  winning, have = rest.split('|')
  return idx, set(winning.split()), set(have.split())


def main():
  scratchcard_list = get_data(today, [('func', parse)])
  lookup = scratchcard_matches(scratchcard_list)
  print(f'{today} star 1 = {sum(map(score, lookup.values()))}')
  print(f'{today} star 2 = {scratchcards_won(lookup)}')


if __name__ == '__main__':
  timed(main)
