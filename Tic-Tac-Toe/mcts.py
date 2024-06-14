# MCTS algorithm implementation


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

