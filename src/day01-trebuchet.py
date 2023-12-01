from santas_little_helpers import day, get_data, timed

today = day(2023, 1)
DIGITS = ["one","two","three","four","five","six","seven","eight","nine"]


def read_calibration_values(document, words=False):
  for line in document:
    nums = []
    for offset in range(len(line)):
      for n, word in enumerate(DIGITS):
        if words and line[offset:].startswith(word):
          nums.append(str(n + 1))
      if line[offset].isdigit():
        nums.append(line[offset])
    yield int(nums[0] + nums[-1])


def main():
  document = list(get_data(today))
  print(f'{today} star 1 = {sum(read_calibration_values(document))}')
  print(f'{today} star 2 = {sum(read_calibration_values(document, words=True))}')


if __name__ == '__main__':
  timed(main)
