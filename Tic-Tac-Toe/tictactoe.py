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
        board.position[row, col] = self.player_1
        # swap players
        (board.player_1, board.player_2) = (board.player_2, board.player_1)

        # return new board state
        return board

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
    print(board)
    # make move on board : this also swaps the player_1 with x or o alternatively
    board = board.make_move(0, 0)

    print(board)
    # print(board.__dict__)
    # board_1 = Board(board)

    # print func implicitly call __str__ func and __str__ returns a human readable string
    # print(board_1)
    # print(board_1.__dict__)
