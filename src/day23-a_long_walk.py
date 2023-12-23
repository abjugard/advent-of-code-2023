from santas_little_helpers import day, get_data, timed
from santas_little_classes import Point, Origo
from santas_little_utils import build_dict_map
import networkx as nx

today = day(2023, 23)

arrows = {'>': Origo.e, '^': Origo.n, '<': Origo.w, 'v': Origo.s}


def optimise_graph(G, the_map, start, end):
  for p in list(G.nodes):
    if p in [start, end]:
      continue
    neighbours = list(G.neighbors(p))
    blocked = G.nodes[p]['blocked']
    if len(neighbours) == 2:
      new_weight = 0
      for n in neighbours:
        new_weight += G[n][p]['weight']
        if G[n][p]['blocked']:
          blocked = G[n][p]['blocked']
      G.add_edge(*neighbours, weight=new_weight, blocked=blocked)
      G.remove_node(p)


def setup_graph(the_map, w, h, directed):
  start = [(x, y) for (x, y), c in the_map.items() if c == '.' and y == 0][0]
  end = [(x, y) for (x, y), c in the_map.items() if c == '.' and y == h-1][0]

  G = nx.grid_graph(dim=(w, h))
  nx.set_edge_attributes(G, 1, 'weight')
  nx.set_edge_attributes(G, None, 'blocked')
  nx.set_node_attributes(G, None, 'blocked')

  for p, c in the_map.items():
    if c == '#':
      G.remove_node(p)
    if c in arrows and directed:
      unreachable = Point(*p)-arrows[c]
      from_node = Point(*p)+arrows[c]
      G.nodes[unreachable.t]['blocked'] = from_node.t

  optimise_graph(G, the_map, start, end)
  if directed:
    G = nx.DiGraph(G)
    for p, n, blocked in list(G.edges.data('blocked', None)):
      if blocked == p:
        G.remove_edge(p, n)

  return G, start, end


def longest_path_to_node(the_map, d, directed=True):
  G, start, end = setup_graph(the_map, *d, directed)
  longest = 0
  for path in nx.all_simple_edge_paths(G, start, end):
    longest = max(longest, sum(G.edges[edge]['weight'] for edge in path))
  return longest


def main():
  the_map, d = build_dict_map(get_data(today))
  print(f'{today} star 1 = {longest_path_to_node(the_map, d)}')
  print(f'{today} star 2 = {longest_path_to_node(the_map, d, directed=False)}')


if __name__ == '__main__':
  timed(main)
