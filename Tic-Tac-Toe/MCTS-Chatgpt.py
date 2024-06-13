import random
import math

# Define the game (Tic-Tac-Toe)
class TicTacToe:
    def __init__(self):
        self.board = [0] * 9  # 0 for empty, 1 for X, -1 for O
        self.current_player = 1  # 1 for X, -1 for O

    def get_legal_moves(self):
        return [i for i in range(9) if self.board[i] == 0]

    def make_move(self, move):
        self.board[move] = self.current_player
        self.current_player = -self.current_player

    def is_terminal(self):
        return self.get_winner() is not None or not any(x == 0 for x in self.board)

    def get_winner(self):
        lines = [
            [self.board[0], self.board[1], self.board[2]],
            [self.board[3], self.board[4], self.board[5]],
            [self.board[6], self.board[7], self.board[8]],
            [self.board[0], self.board[3], self.board[6]],
            [self.board[1], self.board[4], self.board[7]],
            [self.board[2], self.board[5], self.board[8]],
            [self.board[0], self.board[4], self.board[8]],
            [self.board[2], self.board[4], self.board[6]],
        ]
        for line in lines:
            if sum(line) == 3:
                return 1  # X wins
            if sum(line) == -3:
                return -1  # O wins
        if not any(x == 0 for x in self.board):
            return 0  # Draw
        return None

    def clone(self):
        clone = TicTacToe()
        clone.board = self.board[:]
        clone.current_player = self.current_player
        return clone

class Node:
    def __init__(self, game, parent=None):
        self.game = game
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = game.get_legal_moves()

    def expand(self):
        move = self.untried_moves.pop()
        next_game = self.game.clone()
        next_game.make_move(move)
        child_node = Node(next_game, parent=self)
        self.children.append(child_node)
        return child_node

    def best_child(self, exploration_value=1.41):
        choices_weights = [
            (child.wins / child.visits) + exploration_value * math.sqrt((2 * math.log(self.visits) / child.visits))
            for child in self.children
        ]
        return self.children[choices_weights.index(max(choices_weights))]

    def update(self, result):
        self.visits += 1
        self.wins += result

def rollout_policy(game):
    possible_moves = game.get_legal_moves()
    return random.choice(possible_moves)

def simulate(game):
    while not game.is_terminal():
        move = rollout_policy(game)
        game.make_move(move)
    winner = game.get_winner()
    if winner is None:
        return 0
    return winner

def backpropagate(node, result):
    while node is not None:
        node.update(result)
        node = node.parent

def monte_carlo_tree_search(root):
    for _ in range(1000):  # Adjust the number of iterations for better results
        node = root
        # Selection
        while node.untried_moves == [] and node.children != []:
            node = node.best_child()

        # Expansion
        if node.untried_moves != []:
            node = node.expand()

        # Simulation
        result = simulate(node.game)

        # Backpropagation
        backpropagate(node, result)

    return root.best_child(exploration_value=0).game

# Example usage
if __name__ == "__main__":
    initial_game = TicTacToe()
    root = Node(initial_game)
    best_game_state = monte_carlo_tree_search(root)
    print("Best move leads to board state:")
    print(best_game_state.board)
