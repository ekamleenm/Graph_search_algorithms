from copy import deepcopy
from mcts import *


# Tic Tac Board class
class Board:
    def __init__(self, board=None):
        self.player_1 = 'x'
        self.player_2 = 'o'
        self.empty_square = '.'
        self.position = {}

        # init (reset) board
        self.init_board()
        # deep copy of previous board state if available
        if board is not None:
            self.__dict__ = deepcopy(board.__dict__)

    def init_board(self):
        for row in range(3):
            for col in range(3):
                # set every board square to empty square
                self.position[row, col] = self.empty_square

    # make move func
    def make_move(self, row, col):
        # deepcopy the previous board
        board = Board(self)
        board.position[row, col] = self.player_1  # self.player_1  can be o or x
        # swap players
        (board.player_1, board.player_2) = (board.player_2, board.player_1)

        # return new board state
        return board

    def is_draw(self):
        # loop over board squares
        for row, col in self.position:
            if self.position[row, col] == self.empty_square:
                # this is not draw
                return False

        return True  # there is a draw

    def is_win(self):
        # vertical sequence detection
        for col in range(3):
            winning_sequence = []
            for row in range(3):
                if self.position[row, col] == self.player_2:
                    # update winning sequence
                    winning_sequence.append((row, col))

                # if we have 3 elements in row
                if len(winning_sequence) == 3:
                    # the game is won
                    return True

        # horizontal sequence detection
        for row in range(3):
            winning_sequence = []
            for col in range(3):
                if self.position[row, col] == self.player_2:
                    # update winning sequence
                    winning_sequence.append((row, col))

                # if we have 3 elements in row
                if len(winning_sequence) == 3:
                    # the game is won
                    return True

        # 1st diagonal sequence detection
        winning_sequence = []
        for row in range(3):
            col = row
            if self.position[row, col] == self.player_2:
                # update winning sequence
                winning_sequence.append((row, col))

                # if we have 3 elements in row
            if len(winning_sequence) == 3:
                # the game is won
                return True
        # 2nd diagonal sequence detection
        winning_sequence = []
        for row in range(3):
            col = row
            if self.position[row, 2 - col] == self.player_2:
                # update winning sequence
                winning_sequence.append((row, col))

                # if we have 3 elements in row
            if len(winning_sequence) == 3:
                # the game is won
                return True

        return False

    # generate legal moves/states in the current position
    def generate_states(self):
        # define states list (move-list ; list of available actions to consider)
        actions = []  # list of board class instances
        for row in range(3):
            for col in range(3):
                # make sure that current square is empty
                if self.position[row, col] == self.empty_square:
                    # append available action/ board state to action list
                    actions.append(self.make_move(row, col))

        return actions

    # print the board
    def __str__(self):
        # define board string representation
        board_string = ''

        for row in range(3):
            for col in range(3):
                board_string += '%s' % self.position[row, col]

            board_string += '\n'
        # prepend side to move
        if self.player_1 == 'x':
            board_string = "\n---------------\n'x' to move: \n---------------\n\n" + board_string
        elif self.player_1 == 'o':
            board_string = "\n---------------\n'o' to move: \n---------------\n\n" + board_string
        return board_string

    def game_loop(self):
        print('\n Tic Tac Toe Using Monte Carlo Tree Search -- reinforcement learning\n')
        print('   Type exit to quit')
        print('   Move format x,y where x is col and y is row')

        print(self)

        # game loop
        while True:
            # user input
            user_input = input('> ')
            # escape condition
            if user_input == 'exit':
                break

            if user_input == '':
                continue
            # parse user_input (move format: 1,2 ; col,row)
            try:
                row = int(user_input.split(',')[-1]) - 1
                col = int(user_input.split(',')[0]) - 1

                if self.position[row, col] != self.empty_square:
                    print('illegal move\n')
                    continue
                # make move on board
                self = self.make_move(row, col)

                # make AI move here ....

                print(self)

                # check the game state
                if self.is_win():
                    print('this winner is: ')
                    print('player "%s" has won the game!!' % self.player_2)
                    break

                if self.is_draw():
                    print('Game is drawn!\n')
                    break

            except Exception as e:
                print('illegal command!')
                print('Correct format : x,y --> x is col and y is row')


# main driver
if __name__ == '__main__':
    board = Board()
    # start game loop
    # board.game_loop()

    # create Tree node instance
    root = TreeNode(board, None)

    print(root.__dict__)
