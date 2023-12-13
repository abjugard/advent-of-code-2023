from santas_little_helpers import day, get_data, timed

today = day(2023, 13)


def equal_at(pattern, split, tolerance):
  l, r = pattern[:split][::-1], pattern[split:]
  size = min(split, len(pattern)-split)
  smudges = 0
  for ll, rl in zip(l[:size], r[:size]):
    for lc, rc in zip(ll, rl):
      smudges += lc != rc
      if smudges > tolerance:
        return 0
  return split if smudges == tolerance else 0


def reflection_score(rows, tolerance):
  cols = tuple(zip(*rows))
  left = max(equal_at(cols, i, tolerance) for i in range(1, len(cols)))
  top  = max(equal_at(rows, i, tolerance) for i in range(1, len(rows)))
  return 100 * top + left


def sum_of_reflections(patterns, tolerance=0):
  return sum(reflection_score(pattern, tolerance) for pattern in patterns)


def main():
  patterns = [tuple(pattern) for pattern in get_data(today, groups=True)]
  print(f'{today} star 1 = {sum_of_reflections(patterns)}')
  print(f'{today} star 2 = {sum_of_reflections(patterns, tolerance=1)}')


if __name__ == '__main__':
  timed(main)
