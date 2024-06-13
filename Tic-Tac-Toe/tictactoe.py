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


# main driver
if __name__ == '__main__':
    board = Board()
    print('Initial Board state: ')
    print(board)
    # generate actions
    actions = board.generate_states()

    # for action in actions:
    #     print(action)

    # take action  (make the actual move on board)
    board = actions[0]

    # print the updated board
    print('first generated move has been made on board')
    print(board)

    actions = board.generate_states()
    # print('available states after first move: ')
    # for action in actions:
    #     print(action)

    board = actions[0]
    print(board)

    actions = board.generate_states()
    for action in actions:
        print(action)

