import heapq


class Graph:
    def __init__(self):
        self.edges = {}  # key = Node: value = list of tuples [(child_node,cost_to_reach),(),()]
        self.heuristic_node = {}  # key = Node : value = Heuristic value

    def add_edge_to_graph(self, parent_node, child_node, cost_to_reach):
        if parent_node not in self.edges:
            self.edges[parent_node] = []

        # Sending tuple to list of tuples
        self.edges[parent_node].append((child_node, cost_to_reach))

    def set_heuristic(self, key_node, heuristic_value):
        self.heuristic_node[key_node] = heuristic_value

    def greedy_search(self,start_node,goal_node):
        pass



# Example usage
graph = Graph()
edges = [
    ('Arad', 'Sibiu', 140),
    ('Arad', 'Timisoara', 118),
    ('Arad', 'Zerind', 75),
    ('Zerind', 'Oradea', 71),
    ('Oradea', 'Sibiu', 151),
    ('Timisoara', 'Lugoj', 111),
    ('Lugoj', 'Mehadia', 70),
    ('Mehadia', 'Drobeta', 75),
    ('Drobeta', 'Craiova', 120),
    ('Craiova', 'Rimnicu Vilcea', 146),
    ('Craiova', 'Pitesti', 138),
    ('Rimnicu Vilcea', 'Sibiu', 80),
    ('Rimnicu Vilcea', 'Pitesti', 97),
    ('Pitesti', 'Bucharest', 101),
    ('Sibiu', 'Fagaras', 99),
    ('Fagaras', 'Bucharest', 211),
    ('Bucharest', 'Giurgiu', 90)
]

for edge in edges:
    graph.add_edge(*edge)

heuristics = {
    'Arad': 366,
    'Zerind': 374,
    'Oradea': 380,
    'Sibiu': 253,
    'Timisoara': 329,
    'Lugoj': 244,
    'Mehadia': 241,
    'Drobeta': 242,
    'Craiova': 160,
    'Rimnicu Vilcea': 193,
    'Pitesti': 100,
    'Fagaras': 176,
    'Bucharest': 0,
    'Giurgiu': 77
}

for node, h_value in heuristics.items():
    graph.set_heuristic(node, h_value)

graph.greedy_search('Arad', 'Bucharest')

