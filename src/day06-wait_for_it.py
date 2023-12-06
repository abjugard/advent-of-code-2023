from santas_little_helpers import day, get_data, timed
from santas_little_utils import mul

today = day(2023, 6)


def ways_to_win(t, d):
  for speed in range(t):
    time_travelling = t - speed
    distance = time_travelling*speed
    if distance > d:
      return t - 2*speed + 1


def many_races(times, distances):
  for t, d in zip(times, distances):
    yield ways_to_win(int(t), int(d))


def big_race(times, distances):
  t, d = int(''.join(times)), int(''.join(distances))
  return ways_to_win(t, d)


def parse(line):
  nums = line.split(':')[1]
  return nums.split()


def main():
  inp = list(get_data(today, [('func', parse)]))
  print(f'{today} star 1 = {mul(many_races(*inp))}')
  print(f'{today} star 2 = {big_race(*inp)}')


if __name__ == '__main__':
  timed(main)
