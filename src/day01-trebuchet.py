from santas_little_helpers import day, get_data, timed

today = day(2023, 1)
DIGITS = ["one","two","three","four","five","six","seven","eight","nine"]


def find_num(line, words, reverse=False):
  indices = range(len(line))
  if reverse:
    indices = reversed(indices)
  for idx in indices:
    if line[idx].isdigit():
      return line[idx]
    if words:
      for n, word in enumerate(DIGITS):
        if line[idx:].startswith(word):
          return str(n + 1)


def read_calibration_values(document, words=False):
  for line in document:
    yield int(find_num(line, words) + find_num(line, words, True))


def main():
  document = list(get_data(today))
  print(f'{today} star 1 = {sum(read_calibration_values(document))}')
  print(f'{today} star 2 = {sum(read_calibration_values(document, words=True))}')


if __name__ == '__main__':
  timed(main)
