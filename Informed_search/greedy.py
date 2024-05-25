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

    def greedy_search(self, start_node, goal_node):
        open_list = []
        heapq.heappush(open_list, (self.heuristic_node[start_node], start_node))
        parent_info = {start_node: None}
        reached_nodes_costs = {start_node: 0}

        while open_list:
            current_node = heapq.heappop(open_list)[1]    # Min heuristic value node popped
            if current_node == goal_node:
                return self.generate_path(parent_info, current_node)

            for neighbor, cost in self.edges.get(current_node,[]):
                if neighbor not in reached_nodes_costs or reached_nodes_costs[current_node] + cost < reached_nodes_costs[neighbor]:
                    reached_nodes_costs[neighbor] = reached_nodes_costs[current_node] + cost
                    f_score = self.heuristic_node[neighbor]
                    heapq.heappush(open_list, (f_score,neighbor))
                    parent_info[neighbor] = current_node

        return None

    def generate_path(self,parent_info,current_node):
        path = []
        while current_node is not None:
            path.append(current_node)
            current_node = parent_info[current_node]

        return path[:: -1]


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
    graph.add_edge_to_graph(*edge)

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

generated_path = graph.greedy_search('Arad', 'Bucharest')
print("path: ",generated_path)
