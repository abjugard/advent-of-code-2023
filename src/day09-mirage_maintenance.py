from santas_little_helpers import day, get_data, timed
from itertools import pairwise

today = day(2023, 9)


def extrapolate(history):
  if all(v == history[-1] for v in history):
    return history[-1]
  return history[-1] + extrapolate([r-l for l, r in pairwise(history)])


def main():
  report = list(get_data(today, [('split', ' '), ('map', int)]))
  print(f'{today} star 1 = {sum(extrapolate(hist) for hist in report)}')
  print(f'{today} star 2 = {sum(extrapolate(hist[::-1]) for hist in report)}')


if __name__ == '__main__':
  timed(main)
