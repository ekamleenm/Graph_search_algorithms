from copy import deepcopy


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
        # create new board instance
        board = Board()
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


# main driver
if __name__ == '__main__':
    board = Board()
    # print(board)
    # make move on board : this also swaps the player_1 with x or o alternatively
    # board = board.make_move(0, 0)

    # print(board)
    # board_1 = Board(board)

    # print func implicitly call __str__ func and __str__ returns a human-readable string
    # also deep copy doesn't change the original state code/structure if we make changes to the new structure
    # print(board_1)
    # print(board_1.__dict__)
    board.position = {(0, 0): 'o', (0, 1): 'o', (0, 2): 'x',
                      (1, 0): 'o', (1, 1): 'x', (1, 2): 'x',
                      (2, 0): 'x', (2, 1): 'x', (2, 2): 'o'}

    board.player_2 = 'x'
    print(board)
    print('player_2: "%s"' % board.player_2)

    if board.is_win():
        print('Game is won: ', board.is_win())
    else:
        print('Game is Draw: ', board.is_draw())
