def dfs_iterative(graph_, start_node):
    visited = set()
    stack = [start_node]

    while stack:
        popped_node = stack.pop()
        if popped_node not in visited:
            visited.add(popped_node)
            print(popped_node)

        for children in graph_[popped_node]:
            if children not in stack:
                stack.append(children)


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

dfs_iterative(graph, '5')
