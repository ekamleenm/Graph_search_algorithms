import copy
import random
import time
import sys
import math
from collections import namedtuple

#import numpy as np

GameState = namedtuple('GameState', 'to_move, move, utility, board, moves')


def random_player(game, state):
    """A random player that chooses a legal move at random."""
    return random.choice(game.actions(state)) if game.actions(state) else None


# MonteCarlo Tree Search support

class MCTS:  #Monte Carlo Tree Search implementation
    class Node:
        def __init__(self, state, par=None):
            self.state = copy.deepcopy(state)

            self.parent = par
            self.children = []
            self.visitCount = 0
            self.winScore = 0

        def getChildWithMaxScore(self):
            maxScoreChild = max(self.children, key=lambda x: x.visitCount)
            return maxScoreChild

    def __init__(self, game, state):
        self.root = self.Node(state)
        self.state = state
        self.game = game
        self.exploreFactor = math.sqrt(2)

    def isTerminalState(self, utility, moves):
        print(f"Checking terminal state: utility={utility}, moves={moves}")  # Debugging statement
        return

    def monteCarloPlayer(self, timelimit=4):
        """Entry point for Monte Carlo search"""
        start = time.perf_counter()
        end = start + timelimit
        """Use timer above to apply iterative deepening"""
        while time.perf_counter() < end:
            print("Starting iteration")  # Debugging statement

            # SELECT stage use selectNode()
            print("Selecting node")  # Debugging statement
            leaf = self.selectNode(self.root)
            self.expandNode(leaf)
            if leaf.children:
                new_leaf = random.choice(leaf.children)

                # SIMULATE stage using simulateRandomPlay()
                print("Simulating random play")  # Debugging statement
                simulation_result = self.simulateRandomPlay(new_leaf)
                print(f"Simulation result: {simulation_result}")  # Debugging statement

                # BACKUP stage using backPropagation
                print("Backpropagating")  # Debugging statement
                self.backPropagation(new_leaf, simulation_result)

        winnerNode = self.root.getChildWithMaxScore()
        assert winnerNode is not None
        print(
            f"Winner node with utility={winnerNode.state.utility}, moves={winnerNode.state.moves}")  # Debugging statement
        return winnerNode.state.move

    """selection stage function. walks down the tree using findBestNodeWithUCT()"""

    def selectNode(self, nd):
        node = nd
        print("Your code goes here -3pt")
        while node.children:
            node = self.findBestNodeWithUCT(node)
        return node

    def findBestNodeWithUCT(self, nd):
        """finds the child node with the highest UCT. Parse nd's children and use uctValue() to collect uct's for the
        children....."""
        childUCT = []
        print("Your code goes here -2pt")
        for child in nd.children:
            uct_value = self.uctValue(nd.visitCount, child.winScore, child.visitCount)
            childUCT.append((child, uct_value))

        # child with the maximum UCT value
        best_child = max(childUCT, key=lambda item: item[1])[0]
        return best_child

    def uctValue(self, parentVisit, nodeScore, nodeVisit):
        """compute Upper Confidence Value for a node"""
        if nodeVisit == 0:
            return 0 if self.exploreFactor == 0 else sys.maxsize
        return (nodeScore / nodeVisit) + self.exploreFactor * math.sqrt(math.log(parentVisit) / nodeVisit)

    def expandNode(self, nd):
        """generate the child nodes and append them to nd's children"""
        stat = nd.state
        tempState = GameState(to_move=stat.to_move, move=stat.move, utility=stat.utility, board=stat.board, moves=stat.moves)
        for a in self.game.actions(tempState):
            childNode = self.Node(self.game.result(tempState, a), nd)
            nd.children.append(childNode)

    def simulateRandomPlay(self, nd):
        print("Starting simulateRandomPlay")  # Debugging statement
        # first check win possibility for the current node:
        winStatus = self.game.compute_utility(nd.state.board, nd.state.move, nd.state.board[nd.state.move])
        if winStatus == self.game.k:  #means it is opponent's win
            assert (nd.state.board[nd.state.move] == 'X')
            if nd.parent is not None:
                nd.parent.winScore = -sys.maxsize
            return ('X' if winStatus > 0 else 'O')

        """now roll out a random play down to a terminating state. """

        tempState = copy.deepcopy(nd.state)  # to be used in the following random playout
        to_move = tempState.to_move
        move = None
        while not self.isTerminalState(tempState.utility, tempState.moves):
            actions = self.game.actions(tempState)
            if not actions:
                break
            move = random.choice(actions)
            tempState = self.game.result(tempState, move)
            print("Move made: ", move)

        # Calculate utility after reaching a terminal state
        if move is not None:
            print("tempState.to_move: ", tempState.to_move)
            print('move is : ', move)
            winStatus = self.game.compute_utility(tempState.board, move, tempState.to_move)
        else:
            winStatus = 0  # Handle case when no move was possible

        return ('X' if winStatus > 0 else 'O' if winStatus < 0 else 'N')  # 'N' means tie

    def backPropagation(self, nd, winningPlayer):
        """propagate upword to update score and visit count from
        the current leaf node to the root node."""
        tempNode = nd
        print("Your code goes here -5pt")
        while tempNode is not None:
            tempNode.visitCount += 1
            if winningPlayer != 'N':
                if winningPlayer == tempNode.state.to_move:
                    tempNode.winScore += 1
                else:
                    tempNode.winScore -= 1
            tempNode = tempNode.parent
