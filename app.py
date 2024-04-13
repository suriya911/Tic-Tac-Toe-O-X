import math
import random

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_winner = None

    def print_board(self):
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    @staticmethod
    def print_board_nums():
        number_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return len(self.available_moves())

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        # check the row
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind+1)*3]
        if all([spot == letter for spot in row]):
            return True

        # check the column
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True

        # check diagonals
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True

        return False

def minimax(position, depth, maximizing_player, alpha, beta):
    if position.current_winner is not None:
        return position.current_winner

    if depth == 0 or not position.empty_squares():
        if position.current_winner is None:
            return 0  # Return 0 for a tie
        else:
            return 1 if position.current_winner == 'O' else -1

    if maximizing_player:
        max_eval = -math.inf
        for move in position.available_moves():
            position.make_move(move, 'O')
            eval = minimax(position, depth-1, False, alpha, beta)
            position.board[move] = ' '
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval

    else:
        min_eval = math.inf
        for move in position.available_moves():
            position.make_move(move, 'X')
            eval = minimax(position, depth-1, True, alpha, beta)
            position.board[move] = ' '
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def get_best_move(board):
    best_move = -1
    best_score = -math.inf
    for move in board.available_moves():
        board.make_move(move, 'O')
        score = minimax(board, 3, False, -math.inf, math.inf)
        board.board[move] = ' '
        if score > best_score:
            best_score = score
            best_move = move
    return best_move

def play_game():
    board = TicTacToe()
    print("Welcome to Tic Tac Toe!")
    print("Here is the current board:")
    board.print_board()
    print("To make a move, enter a number from 0-8 as shown below:")
    board.print_board_nums()

    while board.empty_squares():
        if board.current_winner is None:
            if random.choice([True, False]):
                human_move = int(input("Enter your move (0-8): "))
                while human_move not in board.available_moves():
                    print("Invalid move. Please try again.")
                    human_move = int(input("Enter your move (0-8): "))
                board.make_move(human_move, 'X')
            else:
                ai_move = get_best_move(board)
                board.make_move(ai_move, 'O')

            board.print_board()
            if board.current_winner is not None:
                print(board.current_winner + " wins!")
                break
        else:
            print("It's a tie!")
            break

if __name__ == "__main__":
    play_game()
