from santas_little_helpers import day, get_data, timed
from santas_little_utils import *

today = day(2023, 3)


def update_part(manual, p):
  for n in neighbours(p, borders=manual):
    if manual[n] != '.' and not manual[n].isdigit():
      return True
  return False


def parse_manual(manual):
  manual_dict = build_dict_map(manual)[0]
  part_nos = []
  is_part = False
  part = ''
  gears = []
  for y, line in enumerate(manual):
    for x, c in enumerate(line):
      if not c.isdigit():
        if is_part and part != '':
          ps = []
          for xp in range(x-len(part), x):
            ps.append((xp, y))
          part_nos.append((set(ps), int(part)))
        if c == '*':
          gears.append((x, y))
        part = ''
        is_part = False
      if c.isdigit():
        part += c
        if not is_part:
          is_part = update_part(manual_dict, (x, y))

  gear_ratios = []
  for p in gears:
    gn = set(neighbours(p, borders=manual_dict))
    matches = []
    for ns, part_no in part_nos:
      if gn & ns:
        matches.append(part_no)
        continue
    if len(matches) == 2:
      gear_ratios.append(mul(matches))

  return sum(value for _, value in part_nos), sum(gear_ratios)


def main():
  inp = list(get_data(today))
  star1, star2 = parse_manual(inp)
  print(f'{today} star 1 = {star1}')
  print(f'{today} star 2 != {star2}')


if __name__ == '__main__':
  timed(main)
