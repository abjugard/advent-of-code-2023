from collections import deque
from santas_little_helpers import alphabet

directions_8 = [('NW', (-1, -1)), ('N', (0, -1)), ('NE', (1, -1)),
                ('W',  (-1,  0)),                 ('E',  (1,  0)),
                ('SW', (-1,  1)), ('S', (0,  1)), ('SE', (1,  1))]

directions_4 = [('N', (0, -1)), ('W', (-1, 0)), ('E', (1, 0)), ('S', (0, 1))]


def get_iterator(variable):
  try:
    it = iter(variable)
    return it
  except TypeError:
    return get_iterator([variable])


def skip(count, it):
  for _ in range(count):
    next(it)
  return next(it)


def get_last(generator):
  d = deque(generator, maxlen=2)
  d.pop()
  return d.pop()


def tesseract_parse(inp, lookup=True, chars=alphabet.upper()):
  from santas_little_ocr_lib import parse_datastructure, set_to_grid, create_image
  data, boundary = parse_datastructure(inp, lookup)
  try:
    import pytesseract
    image = create_image(data, *boundary)
    return pytesseract.image_to_string(image, config=f'--psm 6 -c tessedit_char_whitelist={chars}').strip()
  except ImportError:
    for line in set_to_grid(data, *boundary):
      print(''.join('█' if c else ' ' for c in line))
    print('for cooler results, please install Pillow and pytesseract\n' \
        + '(along with a tesseract-ocr distribution)')
    return None


def build_dict_map(map_data, conv_func=None, key_func=None, criteria=None):
  the_map = dict()
  def get_value(c, p):
    return c if conv_func is None else conv_func(c, p)
  def get_key(c, p):
    return p if key_func is None else key_func(c, p)
  for y, xs in enumerate(map_data):
    for x, c in enumerate(xs):
      if criteria is None or c in criteria:
        the_map[get_key(c, (x, y))] = get_value(c, (x, y))
    else:
      w = x + 1
  else:
    h = y + 1
  return the_map, (w, h)


def map_frame(w, h):
  for x in range(w):
    yield (x, -1)
    yield (x, w)
  for y in range(h):
    yield (-1, y)
    yield (h, y)
  return


def neighbours(p, borders=None, diagonals=False, labels=False):
  def within_borders(p_n, borders):
    if borders is None:
      return True
    elif isinstance(borders, dict):
      return p_n in borders
    elif isinstance(borders, set):
      return p_n in borders
    elif isinstance(borders, list):
      x_n, y_n = p_n
      h = len(borders)
      return h > 0 and 0 <= y_n < h and 0 <= x_n < len(borders[0])
    raise Exception(f'unknown datastructure: {type(borders)}')
  x, y = p
  for label, (xd, yd) in directions_8 if diagonals else directions_4:
    p_n = x + xd, y + yd
    if within_borders(p_n, borders):
      yield (label, p_n) if labels else p_n


def mul(numbers):
  result = 1
  for n in numbers:
    if n == 0:
      return 0
    result *= n
  return result


def transpose(l):
  return list(map(list, zip(*l)))


def flatten(list_of_lists):
  return [item for l in list_of_lists for item in l]


def ints(num_strings, split=None):
  if split:
    num_strings = [s.strip() for s in num_strings.split(split)]
  return tuple(map(int, num_strings))
