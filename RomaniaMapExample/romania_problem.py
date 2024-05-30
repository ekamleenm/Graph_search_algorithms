from copy import deepcopy
from tkinter import *
from utils import *

import sys
from collections import deque
#sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class Graph:
    """A graph connects nodes (vertices) by edges (links). Each edge can also
    have a length associated with it. The constructor call is something like:
        g = Graph({'A': {'B': 1, 'C': 2})
    this makes a graph with 3 nodes, A, B, and C, with an edge of length 1 from
    A to B,  and an edge of length 2 from A to C. You can also do:
        g = Graph({'A': {'B': 1, 'C': 2}, directed=False)
    This makes an undirected graph, so inverse links are also added. The graph
    stays undirected; if you add more links with g.connect('B', 'C', 3), then
    inverse link is also added. You can use g.nodes() to get a list of nodes,
    g.get('A') to get a dict of links out of A, and g.get('A', 'B') to get the
    length of the link from A to B. 'Lengths' can actually be any object at
    all, and nodes can be any hashable object."""

    def __init__(self, graph_dict=None, directed=True):
        self.graph_dict = graph_dict or {}
        self.directed = directed
        if not directed:
            self.make_undirected()

    def make_undirected(self):
        """Make a digraph into an undirected graph by adding symmetric edges."""
        for a in list(self.graph_dict.keys()):
            for (b, dist) in self.graph_dict[a].items():
                self.connect1(b, a, dist)

    def connect(self, A, B, distance=1):
        """Add a link from A and B of given distance, and also add the inverse
        link if the graph is undirected."""
        self.connect1(A, B, distance)
        if not self.directed:
            self.connect1(B, A, distance)

    def connect1(self, A, B, distance):
        """Add a link from A to B of given distance, in one direction only."""
        self.graph_dict.setdefault(A, {})[B] = distance

    def get(self, a, b=None):
        """Return a link distance or a dict of {node: distance} entries.
        .get(a,b) returns the distance or None;
        .get(a) returns a dict of {node: distance} entries, possibly {}."""
        links = self.graph_dict.setdefault(a, {})
        if b is None:
            return links
        else:
            return links.get(b)

    def nodes(self):
        """Return a list of nodes in the graph."""
        s1 = set([k for k in self.graph_dict.keys()])
        s2 = set([k2 for v in self.graph_dict.values() for k2, v2 in v.items()])
        nodes = s1.union(s2)
        return list(nodes)


def UndirectedGraph(graph_dict=None):
    """Build a Graph where every edge (including future ones) goes both ways."""
    return Graph(graph_dict=graph_dict, directed=False)

class Problem:
    """The abstract class for a formal problem. You should subclass
    this and implement the methods actions and result, and possibly
    __init__, goal_test, and path_cost. Then you will create instances
    of your subclass and solve them with the various search functions."""

    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal. Your subclass's constructor can add
        other arguments."""
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""
        raise NotImplementedError

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        raise NotImplementedError

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal or checks for state in self.goal if it is a
        list, as specified in the constructor. Override this method if
        checking against a single self.goal is not enough."""
        if isinstance(self.goal, list):
            return is_in(state, self.goal)
        else:
            return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2. If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1

    def value(self, state):
        """For optimization problems, each state has a value. Hill Climbing
        and related algorithms try to maximize this value."""
        raise NotImplementedError



class Node:
    """A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state. Also includes the action that got us to this state, and
    the total path_cost (also known as g) to reach the node. Other functions
    may add an f and h value; see best_first_graph_search and astar_search for
    an explanation of how the f and h values are handled. You will not need to
    subclass this class."""

    def __init__(self, state, parent=None, action=None, path_cost=0):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node {}>".format(self.state)

    def __lt__(self, node):
        return self.state < node.state

    def expand(self, problem):
        """List the nodes reachable in one step from this node."""
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        """[Figure 3.10]"""
        next_state = problem.result(self.state, action)
        pathCost = problem.path_cost(self.path_cost, self.state, action, next_state)
        
        next_node = Node(next_state, self, action, pathCost)
        return next_node

    def solution(self):
        """Return the sequence of actions to go from the root to this node."""
        return [node.action for node in self.path()[1:]]

    def path(self):
        """Return a list of nodes forming the path from the root to this node."""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    # We want for a queue of nodes in breadth_first_graph_search or
    # astar_search to have no duplicated states, so we treat nodes
    # with the same state as equal. [Problem: this may not be what you
    # want in other contexts.]

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        # We use the hash value of the state
        # stored in the node instead of the node
        # object itself to quickly search a node
        # with the same state in a Hash Table
        return hash(self.state)



class GraphProblem(Problem):
    """The problem of searching a graph from one node to another."""

    def __init__(self, initial, goal, graph):
        super().__init__(initial, goal)
        self.graph = graph

    def actions(self, A):
        """The actions at a graph node are just its neighbors."""
        return list(self.graph.get(A).keys())

    def result(self, state, action):
        """The result of going to a neighbor is just that neighbor."""
        return action

    def path_cost(self, cost_so_far, A, action, B):
        return cost_so_far + (self.graph.get(A, B) or np.inf)

    def find_min_edge(self):
        """Find minimum value of edges."""
        m = np.inf
        for d in self.graph.graph_dict.values():
            local_min = min(d.values())
            m = min(m, local_min)

        return m

    def h(self, node):
        """h function is straight-line distance from a node's state to goal."""
        locs = getattr(self.graph, 'locations', None)
        if locs:
            if type(node) is str:
                return int(distance(locs[node], locs[self.goal]))

            return int(distance(locs[node.state], locs[self.goal]))
        else:
            return np.inf


""" [Figure 3.2]
Simplified road map of Romania
"""
romania_map = UndirectedGraph(dict(
    Arad=dict(Zerind=75, Sibiu=140, Timisoara=118),
    Bucharest=dict(Urziceni=85, Pitesti=101, Giurgiu=90, Fagaras=211),
    Craiova=dict(Drobeta=120, Rimnicu=146, Pitesti=138),
    Drobeta=dict(Mehadia=75),
    Eforie=dict(Hirsova=86),
    Fagaras=dict(Sibiu=99),
    Hirsova=dict(Urziceni=98),
    Iasi=dict(Vaslui=92, Neamt=87),
    Lugoj=dict(Timisoara=111, Mehadia=70),
    Oradea=dict(Zerind=71, Sibiu=151),
    Pitesti=dict(Rimnicu=97),
    Rimnicu=dict(Sibiu=80),
    Urziceni=dict(Vaslui=142)))
romania_map.locations = dict(
    Arad=(91, 492), Bucharest=(400, 327), Craiova=(253, 288),
    Drobeta=(165, 299), Eforie=(562, 293), Fagaras=(305, 449),
    Giurgiu=(375, 270), Hirsova=(534, 350), Iasi=(473, 506),
    Lugoj=(165, 379), Mehadia=(168, 339), Neamt=(406, 537),
    Oradea=(131, 571), Pitesti=(320, 368), Rimnicu=(233, 410),
    Sibiu=(207, 457), Timisoara=(94, 410), Urziceni=(456, 350),
    Vaslui=(509, 444), Zerind=(108, 531))


root = None
city_coord = {}
romania_problem = None
algo = None
start = None
goal = None
counter = -1
city_map = None
frontier = None
front = None
node = None
next_button = None
explored = None


def create_map(root):
    """This function draws out the required map."""
    global city_map, start, goal
    romania_locations = romania_map.locations
    width = 750
    height = 670
    margin = 5
    city_map = Canvas(root, width=width, height=height)
    city_map.pack()

    # Since lines have to be drawn between particular points, we need to list
    # them separately
    make_line(
        city_map,
        romania_locations['Arad'][0], height - romania_locations['Arad'][1],
        romania_locations['Sibiu'][0], height - romania_locations['Sibiu'][1],
        romania_map.get('Arad', 'Sibiu'))
    make_line(
        city_map,
        romania_locations['Arad'][0], height - romania_locations['Arad'][1],
        romania_locations['Zerind'][0], height - romania_locations['Zerind'][1],
        romania_map.get('Arad', 'Zerind'))
    make_line(
        city_map,
        romania_locations['Arad'][0], height -  romania_locations['Arad'][1],
        romania_locations['Timisoara'][0], height - romania_locations['Timisoara'][1],
        romania_map.get('Arad', 'Timisoara'))
    make_line(
        city_map,
        romania_locations['Oradea'][0], height - romania_locations['Oradea'][1],
        romania_locations['Zerind'][0], height - romania_locations['Zerind'][1],
        romania_map.get('Oradea', 'Zerind'))
    make_line(
        city_map,
        romania_locations['Oradea'][0], height - romania_locations['Oradea'][1],
        romania_locations['Sibiu'][0], height - romania_locations['Sibiu'][1],
        romania_map.get('Oradea', 'Sibiu'))
    make_line(
        city_map,
        romania_locations['Lugoj'][0], height - romania_locations['Lugoj'][1],
        romania_locations['Timisoara'][0], height - romania_locations['Timisoara'][1],
        romania_map.get('Lugoj', 'Timisoara'))
    make_line(
        city_map,
        romania_locations['Lugoj'][0],
        height - romania_locations['Lugoj'][1],
        romania_locations['Mehadia'][0],
        height - romania_locations['Mehadia'][1],
        romania_map.get('Lugoj', 'Mehadia'))
    make_line(
        city_map,
        romania_locations['Drobeta'][0],
        height - romania_locations['Drobeta'][1],
        romania_locations['Mehadia'][0],
        height - romania_locations['Mehadia'][1],
        romania_map.get('Drobeta', 'Mehadia'))
    make_line(
        city_map,
        romania_locations['Drobeta'][0],
        height - romania_locations['Drobeta'][1],
        romania_locations['Craiova'][0],
        height - romania_locations['Craiova'][1],
        romania_map.get('Drobeta', 'Craiova'))
    make_line(
        city_map,
        romania_locations['Pitesti'][0],
        height - romania_locations['Pitesti'][1],
        romania_locations['Craiova'][0],
        height - romania_locations['Craiova'][1],
        romania_map.get('Pitesti', 'Craiova'))
    make_line(
        city_map,
        romania_locations['Rimnicu'][0],
        height - romania_locations['Rimnicu'][1],
        romania_locations['Craiova'][0],
        height - romania_locations['Craiova'][1],
        romania_map.get('Rimnicu', 'Craiova'))
    make_line(
        city_map,
        romania_locations['Rimnicu'][0],
        height - romania_locations['Rimnicu'][1],
        romania_locations['Sibiu'][0],
        height - romania_locations['Sibiu'][1],
        romania_map.get('Rimnicu', 'Sibiu'))
    make_line(
        city_map,
        romania_locations['Rimnicu'][0],
        height - romania_locations['Rimnicu'][1],
        romania_locations['Pitesti'][0],
        height - romania_locations['Pitesti'][1],
        romania_map.get('Rimnicu', 'Pitesti'))
    make_line(
        city_map,
        romania_locations['Bucharest'][0],
        height - romania_locations['Bucharest'][1],
        romania_locations['Pitesti'][0],
        height - romania_locations['Pitesti'][1],
        romania_map.get('Bucharest', 'Pitesti'))
    make_line(
        city_map,
        romania_locations['Fagaras'][0],
        height - romania_locations['Fagaras'][1],
        romania_locations['Sibiu'][0],
        height - romania_locations['Sibiu'][1],
        romania_map.get('Fagaras', 'Sibiu'))
    make_line(
        city_map,
        romania_locations['Fagaras'][0],
        height - romania_locations['Fagaras'][1],
        romania_locations['Bucharest'][0],
        height - romania_locations['Bucharest'][1],
        romania_map.get('Fagaras', 'Bucharest'))
    make_line(
        city_map,
        romania_locations['Giurgiu'][0],
        height - romania_locations['Giurgiu'][1],
        romania_locations['Bucharest'][0],
        height - romania_locations['Bucharest'][1],
        romania_map.get('Giurgiu', 'Bucharest'))
    make_line(
        city_map,
        romania_locations['Urziceni'][0],
        height - romania_locations['Urziceni'][1],
        romania_locations['Bucharest'][0],
        height - romania_locations['Bucharest'][1],
        romania_map.get('Urziceni', 'Bucharest'))
    make_line(
        city_map,
        romania_locations['Urziceni'][0],
        height - romania_locations['Urziceni'][1],
        romania_locations['Hirsova'][0],
        height - romania_locations['Hirsova'][1],
        romania_map.get('Urziceni', 'Hirsova'))
    make_line(
        city_map,
        romania_locations['Eforie'][0],
        height - romania_locations['Eforie'][1],
        romania_locations['Hirsova'][0],
        height - romania_locations['Hirsova'][1],
        romania_map.get('Eforie', 'Hirsova'))
    make_line(
        city_map,
        romania_locations['Urziceni'][0],
        height - romania_locations['Urziceni'][1],
        romania_locations['Vaslui'][0],
        height - romania_locations['Vaslui'][1],
        romania_map.get('Urziceni', 'Vaslui'))
    make_line(
        city_map,
        romania_locations['Iasi'][0],
        height - romania_locations['Iasi'][1],
        romania_locations['Vaslui'][0],
        height - romania_locations['Vaslui'][1],
        romania_map.get('Iasi', 'Vaslui'))
    make_line(
        city_map,
        romania_locations['Iasi'][0],
        height - romania_locations['Iasi'][1],
        romania_locations['Neamt'][0],
        height - romania_locations['Neamt'][1],
        romania_map.get('Iasi', 'Neamt'))

    for city in romania_locations.keys():
        make_rectangle(
            city_map, romania_locations[city][0], height - romania_locations[city][1], margin, city)

    make_legend(city_map)


def make_line(map, x0, y0, x1, y1, distance):
    """This function draws out the lines joining various points."""
    map.create_line(x0, y0, x1, y1)
    map.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=distance)


def make_rectangle(map, x0, y0, margin, city_name):
    """This function draws out rectangles for various points."""
    global city_coord
    rect = map.create_rectangle( x0 - margin, y0 - margin, x0 + margin, y0 + margin, fill="white")
    if "Bucharest" in city_name or "Pitesti" in city_name or "Lugoj" in city_name \
            or "Mehadia" in city_name or "Drobeta" in city_name:
        map.create_text(x0 - 2 * margin, y0 - 2 * margin, text=city_name, anchor=E)
    else:
        map.create_text( x0 - 2 * margin, y0 - 2 * margin, text=city_name, anchor=SE)
    city_coord.update({city_name: rect})


def make_legend(map):
    rect1 = map.create_rectangle(600, 100, 610, 110, fill="white")
    text1 = map.create_text(615, 105, anchor=W, text="Un-explored")

    rect2 = map.create_rectangle(600, 115, 610, 125, fill="orange")
    text2 = map.create_text(615, 120, anchor=W, text="Frontier")

    rect3 = map.create_rectangle(600, 130, 610, 140, fill="red")
    text3 = map.create_text(615, 135, anchor=W, text="Currently Exploring")

    rect4 = map.create_rectangle(600, 145, 610, 155, fill="grey")
    text4 = map.create_text(615, 150, anchor=W, text="Explored")

    rect5 = map.create_rectangle(600, 160, 610, 170, fill="dark green")
    text5 = map.create_text(615, 165, anchor=W, text="Final Solution")


def tree_search(problem):
    """
    Search through the successors of a problem to find a goal.
    The argument frontier should be an empty queue.
    Don't worry about repeated paths to a state. [Figure 3.7]
    This function has been changed to make it suitable for the Tkinter GUI.
    """
    global frontier, counter, node
    if counter == -1:
        frontier = deque()
        frontier.append(Node(problem.initial))
        display_frontier(frontier)

    if counter % 3 == 0 and counter >= 0:
        node = frontier.pop()
        display_current(node)

    if counter % 3 == 1 and counter >= 0:
        if problem.goal_test(node.state):
            return node
        frontier.extend(node.expand(problem))
        display_frontier(frontier)

    if counter % 3 == 2 and counter >= 0:
        display_explored(node)
    return None


def graph_search(problem):
    """
    Search through the successors of a problem to find a goal.
    The argument frontier should be an empty queue.
    If two paths reach a state, only use the first one. [Figure 3.7]
    This function has been changed to make it suitable for the Tkinter GUI.
    """
    global counter, frontier, node, explored
    if counter == -1:
        frontier.append(Node(problem.initial))
        explored = set()

        display_frontier(frontier)
    if counter % 3 == 0 and counter >= 0:
        node = frontier.pop()

        display_current(node)
    if counter % 3 == 1 and counter >= 0:
        if problem.goal_test(node.state):
            return node
        explored.add(node.state)
        frontier.extend(child for child in node.expand(problem)
                        if child.state not in explored and
                        child not in frontier)

        display_frontier(frontier)
    if counter % 3 == 2 and counter >= 0:
        display_explored(node)
    return None


def display_frontier(queue):
    """This function marks the frontier nodes (orange) on the map."""
    global city_map, city_coord
    qu = deepcopy(queue)
    while qu:
        node = qu.pop()
        for city in city_coord.keys():
            if node.state == city:
                city_map.itemconfig(city_coord[city], fill="orange")


def display_current(node):
    """This function marks the currently exploring node (red) on the map."""
    global city_map, city_coord
    city = node.state
    city_map.itemconfig(city_coord[city], fill="red")


def display_explored(node):
    """This function marks the already explored node (gray) on the map."""
    global city_map, city_coord
    city = node.state
    city_map.itemconfig(city_coord[city], fill="gray")


def display_final(cities):
    """This function marks the final solution nodes (green) on the map."""
    global city_map, city_coord
    for city in cities:
        city_map.itemconfig(city_coord[city], fill="green")


def breadth_first_tree_search(problem):
    """Search the shallowest nodes in the search tree first."""
    global frontier, counter, node
    if counter == -1:
        frontier = deque()
        frontier.append(Node(problem.initial))
        display_frontier(frontier)

    if counter % 3 == 0 and counter >= 0:
        node = frontier.popleft()
        display_current(node)

    if counter % 3 == 1 and counter >= 0:
        if problem.goal_test(node.state):
            return node
        frontier.extend(node.expand(problem))
        display_frontier(frontier)

    if counter % 3 == 2 and counter >= 0:
        display_explored(node)

    print("counter = ", counter, "frontier:", len(frontier))

    return None


def depth_first_tree_search(problem):
    """Search the deepest nodes in the search tree first."""
    # This search algorithm might not work in case of repeated paths.
    global frontier, counter, node
    if counter == -1:
        frontier = []  # stack
        frontier.append(Node(problem.initial))
        display_frontier(frontier)

    if counter % 3 == 0 and counter >= 0:
        node = frontier.pop()
        display_current(node)

    if counter % 3 == 1 and counter >= 0:
        if problem.goal_test(node.state):
            return node
        frontier.extend(node.expand(problem))
        display_frontier(frontier)

    if counter % 3 == 2 and counter >= 0:
        display_explored(node)

    print("counter = ", counter, "frontier:", len(frontier))

    return None


def breadth_first_graph_search(problem):
    """[Figure 3.11]"""
    global frontier, node, explored, counter
    if counter == -1:
        node = Node(problem.initial)
        display_current(node)
        if problem.goal_test(node.state):
            return node

        frontier = deque([node])  # FIFO queue

        display_frontier(frontier)
        explored = set()

    if counter % 3 == 0 and counter >= 0:
        node = frontier.popleft()
        display_current(node)
        explored.add(node.state)

    if counter % 3 == 1 and counter >= 0:
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                if problem.goal_test(child.state):
                    return child
                frontier.append(child)
        display_frontier(frontier)

    if counter % 3 == 2 and counter >= 0:
        display_explored(node)

    print("counter = ", counter, "frontier:", len(frontier), "Explored: ", len(explored))

    return None


def depth_first_graph_search(problem):
    """Search the deepest nodes in the search tree first."""
    global counter, frontier, node, explored
    if counter == -1:
        frontier = []  # stack
    if counter == -1:
        frontier.append(Node(problem.initial))
        explored = set()
        display_frontier(frontier)

    if counter % 3 == 0 and counter >= 0:
        node = frontier.pop()
        display_current(node)

    if counter % 3 == 1 and counter >= 0:
        if problem.goal_test(node.state):
            return node
        explored.add(node.state)
        frontier.extend(child for child in node.expand(problem)
                        if child.state not in explored and
                        child not in frontier)

        display_frontier(frontier)

    if counter % 3 == 2 and counter >= 0:
        display_explored(node)

    print("counter = ", counter, "frontier:", len(frontier), "Explored: ", len(explored))

    return None


def best_first_graph_search(problem, f=None):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    global frontier, node, explored, counter

    if counter == -1:
        f = memoize(f or problem.h, 'f')
        node = Node(problem.initial)
        display_current(node)
        if problem.goal_test(node.state):
            return node
        frontier = PriorityQueue('min', f)
        frontier.append(node)
        display_frontier(frontier)
        explored = set()
    if counter % 3 == 0 and counter >= 0:
        node = frontier.pop()
        display_current(node)
        if problem.goal_test(node.state):
            return node
        explored.add(node.state)

    if counter % 3 == 1 and counter >= 0:
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
        display_frontier(frontier)

    if counter % 3 == 2 and counter >= 0:
        display_explored(node)

    print("counter = ", counter, "frontier:", len(frontier), "Explored: ", len(explored))

    return None


def uniform_cost_search(problem):
    """[Figure 3.14]"""
    return best_first_graph_search(problem, lambda node: node.path_cost)


def astar_search(problem, h=None):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n))


#
def on_click():
    """
    This function defines the action of the 'Next' button.
    """
    global algo, counter, next_button, romania_problem, start, goal
    romania_problem = GraphProblem(start.get(), goal.get(), romania_map)
    if "Breadth-First Tree Search" == algo.get():
        node = breadth_first_tree_search(romania_problem)
        if node is not None:
            final_path = node.solution()
            final_path.append(start.get())
            display_final(final_path)
            next_button.config(state="disabled")
        counter += 1
    elif "Depth-First Tree Search" == algo.get():
        node = depth_first_tree_search(romania_problem)
        if node is not None:
            final_path = node.solution()
            final_path.append(start.get())
            display_final(final_path)
            next_button.config(state="disabled")
        counter += 1
    elif "Breadth-First Graph Search" == algo.get():
        node = breadth_first_graph_search(romania_problem)
        if node is not None:
            final_path = node.solution()
            final_path.append(start.get())
            display_final(final_path)
            next_button.config(state="disabled")
        counter += 1
    elif "Depth-First Graph Search" == algo.get():
        node = depth_first_graph_search(romania_problem)
        if node is not None:
            final_path = node.solution()
            final_path.append(start.get())
            display_final(final_path)
            next_button.config(state="disabled")
        counter += 1
    elif "Uniform Cost Search" == algo.get():
        node = uniform_cost_search(romania_problem)
        if node is not None:
            final_path = node.solution()
            final_path.append(start.get())
            display_final(final_path)
            next_button.config(state="disabled")
        counter += 1
    elif "Greedy Search" == algo.get():
        node = best_first_graph_search(romania_problem)
        if node is not None:
            final_path = node.solution()
            final_path.append(start.get())
            display_final(final_path)
            next_button.config(state="disabled")
        counter += 1
    elif "A* - Search" == algo.get():
        node = astar_search(romania_problem)
        if node is not None:
            final_path = node.solution()
            final_path.append(start.get())
            display_final(final_path)
            next_button.config(state="disabled")
        counter += 1


def reset_map():
    global counter, city_coord, city_map, next_button
    counter = -1
    for city in city_coord.keys():
        city_map.itemconfig(city_coord[city], fill="white")
    next_button.config(state="normal")


# TODO: Add more search algorithms in the OptionMenu
if __name__ == "__main__":
    #global algo, start, goal, next_button
    root = Tk()
    root.title("Road Map of Romania")
    root.geometry("850x750+0+00")
    algo = StringVar(root)
    start = StringVar(root)
    goal = StringVar(root)
    algo.set("Breadth-First Tree Search")
    start.set('Arad')
    goal.set('Bucharest')
    cities = sorted(romania_map.locations.keys())
    algorithm_menu = OptionMenu(
        root,
        algo, "Breadth-First Tree Search", "Depth-First Tree Search",
        "Breadth-First Graph Search", "Depth-First Graph Search",
        "Uniform Cost Search", "Greedy Search", "A* - Search")
    Label(root, text="\n Search Algorithm").pack()
    algorithm_menu.pack()
    Label(root, text="\n Start City").pack()
    start_menu = OptionMenu(root, start, *cities)
    start_menu.pack()
    Label(root, text="\n Goal City").pack()
    goal_menu = OptionMenu(root, goal, *cities)
    goal_menu.pack()
    frame1 = Frame(root)
    next_button = Button(
        frame1,
        width=6,
        height=2,
        text="Next",
        command=on_click,
        padx=2,
        pady=2,
        relief=GROOVE)
    next_button.pack(side='right')
    reset_button = Button(
        frame1,
        width=6,
        height=2,
        text="Reset",
        command=reset_map,
        padx=2,
        pady=2,
        relief=GROOVE)
    reset_button.pack(side='right')
    frame1.pack(side='bottom')
    create_map(root)
    root.mainloop()
