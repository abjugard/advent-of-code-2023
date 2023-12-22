from santas_little_helpers import day, get_data, timed
from santas_little_utils import ints
from collections import defaultdict, deque
from itertools import product

today = day(2023, 22)

idx = 0
supports_for, supported_by = defaultdict(set), defaultdict(set)


def play_tetris(bricks):
  settled, brick_q = dict(), deque(bricks)
  while brick_q:
    z_min, z_max, idx, brick = brick_q.popleft()
    max_z, overlaps = 0, []
    for i, (b, z) in settled.items():
      if brick & b:
        mz = max(z)
        max_z = max(max_z, mz)
        overlaps.append((mz, (i, b, z)))
    overlaps = [t for mz, t in overlaps if mz == max_z]
    while idx not in settled:
      zr = range(z_min, z_max)
      if z_min == 1:
        settled[idx] = (brick, zr)
        break
      for o_idx, other, o_zr in overlaps:
        if any(z-1 in o_zr for z in zr):
          settled[idx] = (brick, zr)
          supports_for[o_idx].add(idx)
          supported_by[idx].add(o_idx)
      z_min -= 1
      z_max -= 1


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
  ts = line.split('~')
  (xs, xe), (ys, ye), (zs, ze) = zip(*[ints(t.split(',')) for t in ts])
  ps = product(range(xs, xe+1), range(ys, ye+1))
  idx += 1
  return zs, ze+1, idx, set(ps)


def main():
  bricks = list(sorted(get_data(today, [('func', parse)])))
  brick_ids = set(idx for _, _, idx, _ in bricks)
  play_tetris(bricks)
  print(f'{today} star 1 = {sum(len(chain_reaction(idx, part1=True)) == 0 for idx in brick_ids)}')
  print(f'{today} star 2 = {sum(len(chain_reaction(idx)) for idx in brick_ids)}')


if __name__ == '__main__':
  timed(main)
