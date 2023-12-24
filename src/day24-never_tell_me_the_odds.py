from santas_little_helpers import day, get_data, timed
from santas_little_utils import ints
from sympy import Point, Ray, Symbol, solve_poly_system

today = day(2023, 24)

min_test, max_test = 200000000000000, 400000000000000


def construct_ray(pos, vel):
  p1 = Point(*pos)
  p2 = Point(*[p + v for p, v in zip(pos, vel)])
  return Ray(p1, p2)


def intersects(pos, vel, o_pos, o_vel):
  ray1 = construct_ray(pos[:2], vel[:2])
  ray2 = construct_ray(o_pos[:2], o_vel[:2])

  if ray1.is_parallel(ray2):
    return False
  inter = ray1.intersection(ray2)
  if inter:
    i_x, i_y = inter[0]
    if min_test <= i_x <= max_test and min_test <= i_y <= max_test:
      return True
  return False


def intersections(hail):
  s = 0
  skip = set()
  for eqn in hail:
    for other in hail:
      if eqn == other or (eqn, other) in skip:
        continue
      crosses = intersects(*eqn, *other)
      skip.add((other, eqn))
      s += crosses
  return s


def throw_rock(hail):
  x, y, z, vx, vy, vz = syms = [Symbol(c) for c in 'x y z vx vy vz'.split()]
  eqns = []
  for idx, (pos, vel) in enumerate(hail[:3]):
    x_h, y_h, z_h = pos
    vx_h, vy_h, vz_h = vel
    t = Symbol('t'+str(idx))
    eqns.append(x + t * vx - (x_h + t * vx_h))
    eqns.append(y + t * vy - (y_h + t * vy_h))
    eqns.append(z + t * vz - (z_h + t * vz_h))
    syms.append(t)
  x_rock, y_rock, z_rock, *_ = solve_poly_system(eqns, syms)[0]
  return int(x_rock + y_rock + z_rock)


def parse(parts):
  return tuple(ints(part, ',') for part in parts)


def main():
  hail = list(get_data(today, [('split', ' @ '), ('func', parse)]))
  print(f'{today} star 1 = {intersections(hail)}')
  print(f'{today} star 2 = {throw_rock(hail)}')


if __name__ == '__main__':
  timed(main)
