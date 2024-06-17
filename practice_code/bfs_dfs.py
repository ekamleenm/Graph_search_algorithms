from collections import deque


def bfs(graph, start_node):
    visited = set()

    queue = deque([start_node])

    while queue:
        popped_node = queue.popleft()

        if popped_node not in visited:
            visited.add(popped_node)

        for child in graph[popped_node]:
            if child not in visited:
                queue.append(child)


def dfs(graph, start_node):
    visited = set()
    stack = [start_node]

    while stack:
        popped_node = stack.pop()
        if popped_node not in visited:
            visited.add(popped_node)

        for child in graph(popped_node):
            if child not in visited:
                stack.append(child)
