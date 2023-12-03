from santas_little_helpers import day, get_data, timed
from santas_little_utils import build_dict_map, mul, neighbours

today = day(2023, 3)


def near_symbol(manual, p):
  for n in neighbours(p, borders=manual):
    if manual[n] != '.' and not manual[n].isdigit():
      return True
  return False


def parse_manual(raw_manual):
  manual, (w, _) = build_dict_map(raw_manual)
  part_nos, gears = [], []
  part, is_part = '', False
  for (x, y), c in manual.items():
    if c == '*':
      gears.append((x, y))
    if c.isdigit():
      part += c
      is_part |= near_symbol(manual, (x, y))
    if not c.isdigit() or x == w-1:
      if is_part and part != '':
        ps = set()
        for xp in range(x-len(part), x):
          ps.add((xp, y))
        part_nos.append((ps, int(part)))
      part, is_part = '', False

  yield sum(value for _, value in part_nos)

  gear_ratios = []
  for p in gears:
    gn = set(neighbours(p, borders=manual))
    matches = []
    for ns, part_no in part_nos:
      if gn & ns:
        matches.append(part_no)
        continue
    if len(matches) == 2:
      gear_ratios.append(mul(matches))

  yield sum(gear_ratios)


def main():
  star_gen = parse_manual(get_data(today))
  print(f'{today} star 1 = {next(star_gen)}')
  print(f'{today} star 2 = {next(star_gen)}')


if __name__ == '__main__':
  timed(main)
