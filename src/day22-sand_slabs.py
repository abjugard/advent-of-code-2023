from santas_little_helpers import day, get_data, timed
from santas_little_utils import ints
from collections import defaultdict
from itertools import product

today = day(2023, 22)

idx = 0
supports_for, supported_by = defaultdict(set), defaultdict(set)


def play_tetris(bricks):
  settled = dict()
  for z_min, z_max, idx, brick in sorted(bricks):
    max_z, overlaps = 0, []
    for o_idx, (o_brick, o_zr) in settled.items():
      if brick & o_brick:
        mz = max(o_zr)
        max_z = max(max_z, mz)
        overlaps.append((mz, (o_idx, o_brick, o_zr)))
    skip = z_min-max_z-1 if max_z else z_min-1
    zr = range(z_min-skip, z_max-skip)
    if not max_z:
      settled[idx] = (brick, zr)
    for mz, (o_idx, other, o_zr) in overlaps:
      if mz == max_z and any(z-1 in o_zr for z in zr):
        settled[idx] = (brick, zr)
        supports_for[o_idx].add(idx)
        supported_by[idx].add(o_idx)


def chain_reaction(brick_id, is_falling=set(), part1=False):
  will_fall = set()
  for other_id in supports_for[brick_id]:
    if not supported_by[other_id] - {brick_id} - is_falling:
      will_fall.add(other_id)
  if will_fall and part1:
    return [1]
  sub = set()
  for other_id in will_fall - is_falling:
    sub |= chain_reaction(other_id, is_falling | will_fall | sub)
  return will_fall | sub


def parse(line):
  global idx
  idx += 1
  ts = line.split('~')
  (x_s, x_e), (y_s, y_e), (z_s, z_e) = zip(*[ints(t, split=',') for t in ts])
  return z_s, z_e+1, idx, set(product(range(x_s, x_e+1), range(y_s, y_e+1)))


def main():
  bricks = list(get_data(today, [('func', parse)]))
  brick_ids = set(idx for _, _, idx, _ in bricks)
  play_tetris(bricks)
  print(f'{today} star 1 = {sum(len(chain_reaction(idx, part1=True)) == 0 for idx in brick_ids)}')
  print(f'{today} star 2 = {sum(len(chain_reaction(idx)) for idx in brick_ids)}')


if __name__ == '__main__':
  timed(main)
