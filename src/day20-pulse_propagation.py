from santas_little_helpers import day, get_data, timed
from santas_little_utils import mul
from collections import defaultdict, deque
from math import lcm

today = day(2023, 20)

rx_invoker_period = dict()
pulse_counter = defaultdict(int)


def run_program(state, program, rx_invoker, presses):
  pulses = deque([('button', 'broadcaster', False)])
  while pulses:
    invoker, target, pulse_kind = pulses.popleft()
    pulse_counter[pulse_kind] += 1
    if target not in program:
      continue
    kind, targets = program[target]
    match kind:
      case 'broadcaster':
        for t in targets:
          pulses.append((target, t, pulse_kind))
      case '%':
        if pulse_kind is False:
          curr = state[kind][target] = not state[kind][target]
          for t in targets:
            pulses.append((target, t, curr))
      case '&':
        if target == rx_invoker and invoker not in rx_invoker_period and pulse_kind:
          rx_invoker_period[invoker] = presses
        state[kind][target][invoker] = pulse_kind
        next_pulse_kind = not all(state[kind][target].values())
        for t in targets:
          pulses.append((target, t, next_pulse_kind))


def setup_state(program):
  state = {'%': defaultdict(bool), '&': defaultdict(dict)}
  for invoker, (_, targets) in program.items():
    for target in targets:
      if not target in program:
        rx_invoker = invoker
        continue
      if '&' in program[target]:
        state['&'][target][invoker] = False
  return state, rx_invoker, len(state['&'][rx_invoker])


def star_gen(program):
  state, rx_invoker, rx_invoker_count = setup_state(program)
  presses = 0

  while True:
    presses += 1
    run_program(state, program, rx_invoker, presses)
    if presses == 1000:
      yield mul(pulse_counter.values())
    if len(rx_invoker_period) == rx_invoker_count:
      yield lcm(*rx_invoker_period.values())


def parse(line):
  symbol = line[0]
  name, targets = line[1:].split(' -> ')
  if name == 'roadcaster':
    name = symbol = 'broadcaster'
  return symbol, name, targets.split(', ')


def main():
  program = {n: (s, ts) for s, n, ts in get_data(today, [('func', parse)])}
  star = star_gen(program)
  print(f'{today} star 1 = {next(star)}')
  print(f'{today} star 2 = {next(star)}')


if __name__ == '__main__':
  timed(main)
