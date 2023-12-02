from santas_little_helpers import day, get_data, timed
from collections import defaultdict

today = day(2023, 2)


def possible(games):
  max_r, max_g, max_b = 12, 13, 14
  for game, rounds in games:
    for r, g, b in rounds:
      if r > max_r or g > max_g or b > max_b:
        break
    else:
      yield game


def power_of_cubes(games):
  for game, rounds in games:
    min_r = min_g = min_b = 0
    for r, g, b in rounds:
      min_r = max(min_r, r)
      min_g = max(min_g, g)
      min_b = max(min_b, b)
    yield min_r * min_g * min_b


def parse(line):
  game, line = line.split(": ")
  game = int(game[4:])

  rounds = line.split('; ')
  states = []
  for r in rounds:
    state = defaultdict(int)
    cubes = r.split(", ")
    for cube in cubes:
      amount, colour = cube.split(' ')
      state[colour[0]] = int(amount)
    states.append((state['r'], state['g'], state['b']))

  return game, states


def main():
  games = list(get_data(today, [('func', parse)]))
  print(f'{today} star 1 = {sum(possible(games))}')
  print(f'{today} star 2 = {sum(power_of_cubes(games))}')


if __name__ == '__main__':
  timed(main)
