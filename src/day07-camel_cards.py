from santas_little_helpers import day, get_data, timed
from collections import Counter
from functools import cmp_to_key

today = day(2023, 7)

RANK_ORDER = '23456789TJQKA'
RANK_ORDER_JOKERS = 'J23456789TQKA'


def ordering(h1, h2, ranks):
  for c1, c2 in zip(h1, h2):
    if c1 != c2:
      return ranks.index(c1)-ranks.index(c2)


def get_class(hand, use_jokers):
  c = Counter(hand)
  jokers = 0
  if use_jokers:
    jokers = c['J']
    del c['J']
    if jokers == 5:
      return 6
  counts = c.values()

  two_pairs = len([v for v in counts if v == 2]) == 2
  if 5 in counts or max(counts) + jokers == 5: return 6
  if 4 in counts or max(counts) + jokers == 4: return 5
  if two_pairs and jokers == 1:                return 4
  if 3 in counts and 2 in counts:              return 4
  if jokers == 2:                              return 3
  if 3 in counts:                              return 3
  if 2 in counts and jokers == 1:              return 3
  if two_pairs:                                return 2
  if jokers == 1:                              return 1
  if 2 in counts:                              return 1
  return 0


def cmp_func(jokers=False):
  def __compare__(t1, t2):
    h1, h2 = t1[0], t2[0]
    h1_c = get_class(h1, use_jokers=jokers)
    h2_c = get_class(h2, use_jokers=jokers)
    if h1_c != h2_c:
      return h1_c-h2_c
    else:
      ranks = RANK_ORDER_JOKERS if jokers else RANK_ORDER
      return ordering(h1, h2, ranks)
  return __compare__


def winnings(tuples, jokers=False):
  tuples = sorted(tuples, key=cmp_to_key(cmp_func(jokers)))
  for idx, (_, bid) in enumerate(tuples):
    yield (idx + 1) * bid


def parse(line):
  hand, bet = line.split()
  return hand, int(bet)


def main():
  tuples = list(get_data(today, [('func', parse)]))
  print(f'{today} star 1 = {sum(winnings(tuples))}')
  print(f'{today} star 2 = {sum(winnings(tuples, jokers=True))}')


if __name__ == '__main__':
  timed(main)
