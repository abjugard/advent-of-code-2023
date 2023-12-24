from santas_little_helpers import day, get_data, timed
from santas_little_utils import ints
from sympy import Point, Ray, Symbol, solve_poly_system
from itertools import combinations

today = day(2023, 24)

min_test, max_test = 2e14, 4e14


def construct_ray(pos, vel):
  p1 = Point(*pos)
  p2 = Point(*[p + v for p, v in zip(pos, vel)])
  return Ray(p1, p2)


def intersects(pos, vel, o_pos, o_vel):
  ray1 = construct_ray(pos[:2], vel[:2])
  ray2 = construct_ray(o_pos[:2], o_vel[:2])

  if ray1.is_parallel(ray2):
    return False
  if intersection := ray1.intersection(ray2):
    i_x, i_y = intersection[0]
    if min_test <= i_x <= max_test and min_test <= i_y <= max_test:
      return True
  return False


def intersections(hail):
  return sum(intersects(*eqn, *o_eqn) for eqn, o_eqn in combinations(hail, 2))


def throw_rock(hail):
  s_syms = [Symbol(c) for c in 'x y z'.split()]
  v_syms = [Symbol(c) for c in 'vx vy vz'.split()]
  eqns, syms = [], s_syms + v_syms
  for idx, (pos, vel) in enumerate(hail[:3]):
    t = Symbol(f't{idx}')
    for s, v, s_h, v_h in zip(s_syms, v_syms, pos, vel):
      eqns.append(s + t * v - (s_h + t * v_h))
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
