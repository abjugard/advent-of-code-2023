from santas_little_helpers import day, get_data, timed
from functools import cache

today = day(2023, 12)


@cache
def possible_arrangements(pattern, broken_groups):
  if len(broken_groups) == 0:
    return '#' not in pattern

  current_len, *rest_groups = broken_groups
  min_tail = len(rest_groups) + sum(rest_groups)

  s = 0
  for prefix_len in range(len(pattern) - current_len - min_tail + 1):
    current = '.' * prefix_len + '#' * current_len + '.'
    if all(p == c or p == '?' for p, c in zip(pattern, current)):
      s += possible_arrangements(pattern[len(current):], tuple(rest_groups))
  return s


def total_arrangement_counts(records, unfolds=1):
  s = 0
  for pattern, broken_groups in records:
    pattern = '?'.join([pattern]*unfolds)
    broken_groups = broken_groups*unfolds
    s += possible_arrangements(pattern, broken_groups)
  return s


def parse(line):
  pattern, broken_groups = line.split()
  broken_groups = tuple(map(int, broken_groups.split(',')))
  return f'{pattern}', broken_groups


def main():
  records = list(get_data(today, [('func', parse)]))
  print(f'{today} star 1 = {total_arrangement_counts(records)}')
  print(f'{today} star 2 = {total_arrangement_counts(records, unfolds=5)}')


if __name__ == '__main__':
  timed(main)
