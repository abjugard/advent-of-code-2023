from dataclasses import dataclass
from types import SimpleNamespace


class NestedNamespace(SimpleNamespace):
  def __init__(self, dictionary, **kwargs):
    super().__init__(**kwargs)
    for key, value in dictionary.items():
      self.__setattr__(key, self.__get_entry__(value))

  def __getattr__(self, key):
    return self.default

  def __get_entry__(self, value):
    if isinstance(value, dict):
      return NestedNamespace(value)
    elif isinstance(value, list):
      return [self.__get_entry__(item) for item in value]
    else:
      return value

  def to_dict(self):
    return self.__dict__


@dataclass
class Point:
  x: int = 0
  y: int = 0


  def __add__(self, other):
    return Point(self.x + other.x, self.y + other.y)
  def __sub__(self, other):
    return Point(self.x - other.x, self.y - other.y)
  def __eq__(self, other):
    return self.x == other.x and self.y == other.y
  def __lt__(self, other):
    if self.y < other.y:
      return True
    if self.y > other.y:
      return False
    return self.x < other.x
  def __hash__(self):
    return 2971215073 * self.x + 433494437 * self.y
  def __iter__(self):
    yield self.x
    yield self.y


  @property
  def n  (self): return Point(self.x,   self.y-1)
  @property
  def ne (self): return Point(self.x+1, self.y-1)
  @property
  def e  (self): return Point(self.x+1, self.y)
  @property
  def se (self): return Point(self.x+1, self.y+1)
  @property
  def s  (self): return Point(self.x,   self.y+1)
  @property
  def sw (self): return Point(self.x-1, self.y+1)
  @property
  def w  (self): return Point(self.x-1, self.y)
  @property
  def nw (self): return Point(self.x-1, self.y-1)

  def next(self, d):
    match d:
      case 'N': return self.n
      case 'E': return self.e
      case 'W': return self.w
      case 'S': return self.s


  @property
  def t(self):
    return (self.x, self.y)
  @property
  def copy(self):
    return Point(self.x, self.y)


  @property
  def direct_neighbours(self):
    return set([self.n, self.e, self.s, self.w])
  @property
  def neighbours(self):
    return [self.nw, self.n, self.ne,
            self.w,          self.e,
            self.sw, self.s, self.se]


  def move(self, other, multiplier=1):
    self.x += other.x * multiplier
    self.y += other.y * multiplier
    return self


  def distance_to(self, other):
    return abs(self.x-other.x), abs(self.y-other.y)


  def manhattan_distance_to(self, other):
    return abs(self.x-other.x) + abs(self.y-other.y)


  def is_neighbour(self, other):
    dx, dy = self.distance_to(other)
    return dx <= 1 and dy <= 1


Origo = Point()
