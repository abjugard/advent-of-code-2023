from santas_little_helpers import day, get_data, timed
from santas_little_classes import NestedNamespace
from santas_little_utils import mul
from operator import gt, lt

today = day(2023, 19)


def adjust_ranges(token, cmp, value, range_groups, inverse=False):
  adjusted = []
  for ranges in range_groups:
    low, high = ranges[token]
    if (cmp is gt) ^ inverse:
      low = max(low, value + (not inverse))
    else:
      high = min(high, value - (not inverse))
    if low > high:
      continue
    ranges[token] = (low, high)
    adjusted.append(ranges)
  return adjusted


def get_rating_ranges_rec(rules):
  rule, *rest = rules
  if rule.conditions is None:
    return get_rating_ranges(rule.next_rule)
  rule_ranges = adjust_ranges(*rule.conditions, get_rating_ranges(rule.next_rule))
  rest_ranges = adjust_ranges(*rule.conditions, get_rating_ranges_rec(rest), inverse=True)
  return rule_ranges + rest_ranges


def get_rating_ranges(curr='in'):
  match curr:
    case 'A':
      return [{c: (1, 4000) for c in 'xmas'}]
    case 'R':
      return []
  return get_rating_ranges_rec(workflows[curr])


def distinct_combinations():
  s = 0
  for ranges in get_rating_ranges():
    s += mul([high - low + 1 for low, high in ranges.values()])
  return s


def get_rating(rating, curr='in'):
  while curr not in 'AR':
    workflow = workflows[curr]
    for r in workflow:
      if r.conditions is not None:
        token, cmp, value = r.conditions
        if cmp(rating[token], value):
          curr = r.next_rule
          break
      curr = r.next_rule
  return sum(rating.values()) if curr == 'A' else 0


def parse_ratings(line):
  items = line[1:-1].split(',')
  rating = {item[0]: int(item[2:]) for item in items}
  return rating


def parse_workflows(workflows):
  d = dict()
  for line in workflows:
    name, contents = line[:-1].split('{')
    d[name] = rules = []
    for r_string in contents.split(','):
      rule = dict()
      if ':' in r_string:
        conds, rule['next_rule'] = r_string.split(':')
        op = gt if conds[1] == '>' else lt
        rule['conditions'] = (conds[0], op, int(conds[2:]))
      else:
        rule['next_rule'] = r_string
        rule['conditions'] = None
      rules.append(NestedNamespace(rule))
  return d


def parse(inp):
  workflows = parse_workflows(next(inp))
  ratings = [parse_ratings(rating) for rating in next(inp)]
  return workflows, ratings


def main():
  global workflows
  workflows, ratings = parse(get_data(today, groups=True))
  print(f'{today} star 1 = {sum(get_rating(rating) for rating in ratings)}')
  print(f'{today} star 2 = {distinct_combinations()}')


if __name__ == '__main__':
  timed(main)
