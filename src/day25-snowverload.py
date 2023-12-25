from santas_little_helpers import day, get_data, timed
from santas_little_utils import mul
import networkx as nx

today = day(2023, 25)


def disconnect_components(links):
  G = nx.Graph()
  for l, t in links:
    for r in t:
      G.add_edge(l, r)
  for link in nx.minimum_edge_cut(G):
    G.remove_edge(*link)
  return mul(map(len, nx.connected_components(G)))


def parse(line):
  l, r = line.split(': ')
  return l, r.split()


def main():
  links = get_data(today, [('func', parse)])
  print(f'{today} star 1 = {disconnect_components(links)}')


if __name__ == '__main__':
  timed(main)
