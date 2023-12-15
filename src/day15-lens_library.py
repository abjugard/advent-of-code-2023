from santas_little_helpers import day, get_data, timed
from santas_little_utils import mul
from collections import defaultdict

today = day(2023, 15)


def get_hash(lens):
  hashcode = 0
  for c in lens:
    hashcode += ord(c)
    hashcode *= 17
    hashcode %= 256
  return hashcode


def get_focusing_power(lenses):
  boxes = defaultdict(list)
  for lens in lenses:
    removal = '-' in lens
    if removal:
      label = lens[:-1]
    else:
      label, attr = lens.split('=')
      attr = int(attr)
    box = boxes[get_hash(label)]
    idx = [i for i, (l, _) in enumerate(box) if l == label]
    if removal:
      if idx:
        box.pop(idx[0])
    else:
      if idx:
        box[idx[0]] = (label, attr)
      else:
        box.append((label, attr))

  focusing_power = 0
  for idx, box in boxes.items():
    for l_idx, (_, focal_length) in enumerate(box):
      focusing_power += mul([idx+1, l_idx+1, focal_length])

  return focusing_power


def main():
  lenses = list(next(get_data(today, [('split', ',')])))
  print(f'{today} star 1 = {sum(get_hash(lens) for lens in lenses)}')
  print(f'{today} star 2 = {get_focusing_power(lenses)}')


if __name__ == '__main__':
  timed(main)
