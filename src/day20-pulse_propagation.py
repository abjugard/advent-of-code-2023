from santas_little_helpers import day, get_data, timed
from santas_little_utils import mul
from collections import defaultdict, deque
from math import lcm

today = day(2023, 20)

presses = 0
rx_invoker_period = dict()
pulse_counter = defaultdict(int)


def run_program(state, program, rx_invoker):
  pulses = deque([('button', 'broadcaster', False)])
  while pulses:
    invoker, name, pulse_kind = pulses.popleft()
    pulse_counter[pulse_kind] += 1
    if name not in program:
      continue
    kind, targets = program[name]
    match kind:
      case 'broadcaster':
        for t in targets:
          pulses.append((name, t, pulse_kind))
      case '%':
        if pulse_kind is False:
          curr = state[kind][name] = not state[kind][name]
          for t in targets:
            pulses.append((name, t, curr))
      case '&':
        if name == rx_invoker and invoker not in rx_invoker_period and pulse_kind:
          rx_invoker_period[invoker] = presses
        state[kind][name][invoker] = pulse_kind
        next_pulse_kind = not all(s for s in state[kind][name].values())
        for t in targets:
          pulses.append((name, t, next_pulse_kind))


def setup_state(program):
  state = {'%': defaultdict(bool), '&': defaultdict(dict)}
  for invoker, (_, targets) in program.items():
    for t in targets:
      if not t in program:
        rx_invoker = invoker
        continue
      kind, _ = program[t]
      if kind == '&':
        state['&'][t][invoker] = False
  return state, rx_invoker


def star_gen(program):
  global presses
  state, rx_invoker = setup_state(program)

  while len(rx_invoker_period) < 4:
    presses += 1
    run_program(state, program, rx_invoker)
    if presses == 1000:
      yield mul(pulse_counter.values())

  yield lcm(*rx_invoker_period.values())


def parse(line):
  symbol = line[0]
  name, targets = line[1:].split(' -> ')
  if name == 'roadcaster':
    name = 'broadcaster'
    symbol = 'broadcaster'
  targets = targets.split(', ')
  return symbol, name, targets


def main():
  program = {n: (s, ts) for s, n, ts in get_data(today, [('func', parse)])}
  star = star_gen(program)
  print(f'{today} star 1 = {next(star)}')
  print(f'{today} star 2 = {next(star)}')


if __name__ == '__main__':
  timed(main)
