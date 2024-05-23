from collections import deque


def bfs(graph_, start_node):
    # set created for all the visited nodes
    visited = set()

    # queue initialized with start node.
    # queue has all the non visited nodes.
    queue = deque([start_node])

    while queue:

        popped_node = queue.popleft()  # Dequeue a node from the front of the queue

        if popped_node not in visited:
            visited.add(popped_node)
            print(popped_node)

        for children in graph_[popped_node]:
            if children not in visited:
                queue.append(children)


graph = {
    '5': ['3', '7'],
    '3': ['2', '4'],
    '7': ['8', '9'],
    '2': ['1'],
    '4': [],
    '8': ['10'],
    '9': [],
    '1': [],
    '10': []
}

graph_2 = {'A': [], 'B': [], 'C': []}
bfs(graph_2, 'A')  # Should print: A
bfs(graph, '5')
