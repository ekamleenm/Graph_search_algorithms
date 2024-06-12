import tkinter as tk
from tkinter import messagebox
import numpy as np


class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe with Minimax")
        self.board = np.array([['', '', ''], ['', '', ''], ['', '', '']])
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.depth = 2
        self.create_board()

    def create_board(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.root, text='', font=('normal', 40), width=5, height=2,
                                               command=lambda i=i, j=j: self.on_click(i, j))
                self.buttons[i][j].grid(row=i, column=j)
        reset_button = tk.Button(self.root, text='Reset', font=('normal', 20), command=self.reset_board)
        reset_button.grid(row=3, column=0, columnspan=3)

    def on_click(self, i, j):
        if self.buttons[i][j]['text'] == '' and self.current_player == 'O':
            self.buttons[i][j]['text'] = 'O'
            self.board[i][j] = 'O'
            if self.check_winner():
                messagebox.showinfo("Tic-Tac-Toe", "Player O wins!")
                self.reset_board()
            else:
                self.current_player = 'X'
                self.ai_move()

    def ai_move(self):
        best_move = None
        best_value = float('-inf')
        for child in self.get_children(self.board, 'X'):
            move_value = self.minimax(child, self.depth - 1, False)
            if move_value > best_value:
                best_value = move_value
                best_move = child

        if best_move is not None:
            self.board = best_move
            self.update_board()
            if self.check_winner():
                messagebox.showinfo("Tic-Tac-Toe", "Player X wins!")
                self.reset_board()
            else:
                self.current_player = 'O'

    def update_board(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]['text'] = self.board[i][j]

    def reset_board(self):
        self.board = np.array([['', '', ''], ['', '', ''], ['', '', '']])
        self.current_player = 'O'
        self.update_board()

    def is_terminal(self, board):
        for row in board:
            if row[0] == row[1] == row[2] != '':
                return True, row[0]
        for col in board.T:
            if col[0] == col[1] == col[2] != '':
                return True, col[0]
        if board[0, 0] == board[1, 1] == board[2, 2] != '':
            return True, board[0, 0]
        if board[0, 2] == board[1, 1] == board[2, 0] != '':
            return True, board[0, 2]
        if not any('' in row for row in board):
            return True, 'Draw'
        return False, ''

    def evaluate(self, board):
        terminal, winner = self.is_terminal(board)
        if terminal:
            if winner == 'X':
                return 1
            elif winner == 'O':
                return -1
            else:
                return 0
        return 0

    def get_children(self, board, player):
        children = []
        for i in range(3):
            for j in range(3):
                if board[i, j] == '':
                    new_board = board.copy()
                    new_board[i, j] = player
                    children.append(new_board)
        return children

    def minimax(self, board, depth, maximizingPlayer):
        if depth == 0 or self.is_terminal(board)[0]:
            return self.evaluate(board)

        if maximizingPlayer:
            maxEval = float('-inf')
            for child in self.get_children(board, 'X'):
                eval = self.minimax(child, depth - 1, False)
                maxEval = max(maxEval, eval)
            return maxEval
        else:
            minEval = float('inf')
            for child in self.get_children(board, 'O'):
                eval = self.minimax(child, depth - 1, True)
                minEval = min(minEval, eval)
            return minEval

    def check_winner(self):
        terminal, winner = self.is_terminal(self.board)
        if terminal and winner != 'Draw':
            return True
        return False

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
