# MCTS algorithm implementation

# 10:26 / 25:35

# packages
import math
import random


# tree node class definition
class TreeNode:
    def __init__(self, board, parent=None):
        # init associated board states
        self.board = board

        # is node terminal --> won or drawn(flag)
        if self.board.is_win() or self.board.is_draw():
            # we have the terminal node
            self.terminal = True
        else:
            self.terminal = False

        # fully expanded
        self.is_fully_expanded = self.terminal

        # init parent node if available
        self.parent = parent

        # init score and visits
        self.visits = 0
        self.total_score = 0

        # init current node's children
        self.children = {}


# MCTS class
class MCTS:
    # search for the best move in the current position
    def search(self, initial_state):
        # create root node
        self.root = TreeNode(initial_state, None)

        # search 1000 iterations
        for iterations in range(1000):
            # select a node --> SELECTION PHASE
            node = self.select(self.root)

            # SIMULATION PHASE
            score = self.rollout(node.board)

            # Backpropagation : the score the # visits and score to the root node
            self.backpropogate(node, score)

            # pickup the best move in the current position
            try:
                return self.get_best_move(self.root, 0)
            except Exception as e:
                pass

    # select most promising node
    def select(self, node):
        # make sure that we are dealing with non-terminal nodes
        while not node.is_terminal:
            # case : when node is fully expanded
            if node.is_fully_expanded:
                node = self.get_best_move(node, 2)

            # case : when the node is not fully expanded
            else:
                return self.expand(node)

        return node

    # simulate the game by making random moves until reach end of the game
    def rollout(self, board):
        # make random moves for both sides until terminal state of the game is reached
        while not board.is_win():
            # try to make a move
            try:
                # make the move on board
                board = random.choice(board.generate_states())
            except Exception as e:
                print(board)
                print("Draw State: ", board.is_draw())
                return 0

        print(board)
        # return score from player x pov
        if board.player_2 == 'x':
            print('winner: ', board.player_2)
            return 1
        elif board.player_2 == 'o':
            print('winner: ', board.player_2)
            return -1

    def backpropogate(self, node, score):
        pass

    def expand(self, node):
        # generate the legal states/moves for the current (node)
        states = node.board.generate_states()
        # loop over generates states
        for state in states:
            # make sure that current state is not present in child_nodes {}
            if str(state.position) not in node.children:
                # create a new node
                new_node = TreeNode(state, node)

                # add child node to parent's node children list (actually dictionary)
                node.children[str(state.position)] = new_node
                # whether current node (parameter node) is fully expanded or not
                if len(states) == len(node.children):
                    node.is_fully_expanded = True

                # return new node
                return new_node

    # Select the best node bases on UCB1/UCT formula
    # we need to loop over child nodes of the below node taken as parameter
    def get_best_move(self, node, exploration_constant):
        # define best score and best moves
        best_score = float('-inf')
        best_moves = []

        # loop over child nodes
        for child_node in node.children.values():
            # define current player
            if child_node.board.player_2 == 'x':
                current_player = 1
            if child_node.board.player_2 == 'o':
                current_player = -1

            # get move score using UCT formula
            move_score = current_player * child_node.score / child_node.visits + exploration_constant * math.sqrt(
                math.log(node.visits) / child_node.visits)

            # better move has been found
            if move_score > best_score:
                best_score = move_score
                best_moves = [child_node]

            # found as good move as already available
            elif move_score == best_score:
                best_moves.append(child_node)

        # return one of the best moves randomly
        return random.choice(best_moves)
