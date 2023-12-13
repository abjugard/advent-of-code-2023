from santas_little_helpers import day, get_data, timed

today = day(2023, 13)


def equal(l, r, tolerance=0):
  size = min(len(l), len(r))
  l, r = l[::-1][:size], r[:size]
  smudges = 0
  for ll, rl in zip(l, r):
    for lc, rc in zip(ll, rl):
      if lc != rc:
        smudges += 1
      if smudges > tolerance:
        return False
  return smudges == tolerance or tolerance == 0


def score(rows, tolerance=0):
  cols = [''.join(x) for x in zip(*rows)]
  left = 0
  for i in range(len(cols)):
    if equal(cols[:i], cols[i:], tolerance):
      left = i
  top = 0
  for i in range(len(rows)):
    if equal(rows[:i], rows[i:], tolerance):
      top = i
  return 100 * top + left


def sum_of_reflections(patterns, tolerance=0):
  return sum(score(pattern, tolerance) for pattern in patterns)


def main():
  patterns = get_data(today, groups=True)
  patterns = [list(pattern) for pattern in patterns]
  print(f'{today} star 1 = {sum_of_reflections(patterns)}')
  print(f'{today} star 2 = {sum_of_reflections(patterns, tolerance=1)}')


if __name__ == '__main__':
  timed(main)
