import heapq


def ucs(graph_, start_node, goal_node):
    visited = set()
    priority_queue = [(0, start_node, [])]  # Initialize with a tuple (cost, start_node, path)

    while priority_queue:
        cost, current_node, path = heapq.heappop(priority_queue)

        if current_node in visited:
            continue

        visited.add(current_node)
        path = path + [current_node]

        if current_node == goal_node:
            return cost, path

        # Exploring the children
        for child_node, cost_to_be in graph_.get(current_node, []):
            if child_node not in visited:
                heapq.heappush(priority_queue, (cost + cost_to_be, child_node, path))


# Example graph with edge costs
graph = {
    'A': [('B', 1), ('C', 4)],
    'B': [('A', 1), ('D', 2), ('E', 5)],
    'C': [('A', 4), ('F', 3)],
    'D': [('B', 2)],
    'E': [('B', 5), ('F', 1)],
    'F': [('C', 3), ('E', 1)]
}

# Test the UCS function
result = ucs(graph, 'A', 'F')
# Output should be the minimum cost and path to the goal node
print(result)

