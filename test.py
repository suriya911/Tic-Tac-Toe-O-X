from flask import Flask, render_template, request
import random

app = Flask(__name__)


class TicTacToe:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]

    @staticmethod
    def print_board(self):
        for row in self.board:
            print('|'.join(row))
            print('-' * 5)

    def check_winner(self, player):
        for row in self.board:
            if all(cell == player for cell in row):
                return True
        for col in range(3):
            if all(self.board[row][col] == player for row in range(3)):
                return True
        if all(self.board[i][i] == player for i in range(3)) or all(self.board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def game_over(self, human, pc):
        return self.check_winner(human) or self.check_winner(pc) or \
            all(self.board[row][col] != ' ' for row in range(3)
                for col in range(3))

    def evaluate(self, human, pc):
        if self.check_winner(human):
            return 1
        elif self.check_winner(pc):
            return -1
        else:
            return 0

    def empty_cells(self):
        return [(row, col) for row in range(3) for col in range(3) if self.board[row][col] == ' ']

    def empty_board(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]


class TicTacToeAI:
    def __init__(self, game):
        self.game = game

    def minimax(self, depth, alpha, beta, maximizing_player, human, pc):
        if self.game.game_over(human, pc) or depth == 0:
            return self.game.evaluate(human, pc), None

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for row, col in self.game.empty_cells():
                self.game.board[row][col] = 'X'
                eval, _ = self.minimax(
                    depth - 1, alpha, beta, False, human, pc)
                self.game.board[row][col] = ' '
                max_eval = max(max_eval, eval)
                if max_eval >= beta:
                    break
                if max_eval > alpha:
                    alpha = max_eval
                    best_move = (row, col)
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for row, col in self.game.empty_cells():
                self.game.board[row][col] = 'O'
                eval, _ = self.minimax(depth - 1, alpha, beta, True, human, pc)
                self.game.board[row][col] = ' '
                min_eval = min(min_eval, eval)
                if min_eval <= alpha:
                    break
                if min_eval < beta:
                    beta = min_eval
                    best_move = (row, col)
            return min_eval, best_move


def start_game():
    game = TicTacToe()
    ai = TicTacToeAI(game)
    print("Welcome to Tic-Tac-Toe!")
    game.print_board()
    play = True
    while (play == True):
        print("Starting game...")
        print("Tossing to decide who goes first...")
        toss = random.choice(
            [False, True, True, False, True, False, False, False, True, True, False, True])
        if toss == True:
            print("You go first!")
            human = 'X'
            pc = 'O'
        else:
            print("AI goes first!")
            human = 'O'
            pc = 'X'
        start = 1 if toss else -1
        depth = 3  # Starting depth
        while not game.game_over(human, pc):

            if start == 1:

                # Human's turn
                row, col = get_human_move(game)
                game.board[row][col] = human
                game.print_board()

                if game.game_over(human, pc):
                    break

                # AI's turn with iterative deepening
                print("AI is thinking...")
                _, (row, col) = ai.minimax(depth, float(
                    '-inf'), float('inf'), True, human, pc)
                game.board[row][col] = pc
                print(f"AI placed an {pc} at position: {row, col}")
                game.print_board()
            else:
                # AI's turn with iterative deepening
                print("AI is thinking...")
                _, (row, col) = ai.minimax(depth, float(
                    '-inf'), float('inf'), True, human, pc)
                game.board[row][col] = pc
                print(f"AI placed an {pc} at position: {row, col}")
                game.print_board()

                if game.game_over(human, pc):
                    break

                # Human's turn
                row, col = get_human_move(game)
                game.board[row][col] = human
                game.print_board()

            # Increase depth for deeper search
            depth += 1

        winner = game.evaluate(human, pc)
        if winner == 1:
            print("Congratulations! You won!")
        elif winner == -1:
            print("AI wins!")
        else:
            print("It's a draw!")
        game.empty_board()
        play = input("Do you want to play again? (y/n): ").lower() == 'y'
    print("Thanks for playing!")


def get_human_move(game):
    while True:
        try:
            row, col = map(int, input("Enter row and column: ").split())
            if game.board[row][col] == ' ':
                return row, col
            else:
                print("That position is already taken. Try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/play', methods=['POST'])
def play():
    game = TicTacToe()
    ai = TicTacToeAI(game)
    toss = random.choice(
            [False, True, True, False, True, False, False, False, True, True, False, True])
    if toss == True:
        print("You go first!")
        human = 'X'
        pc = 'O'
    else:
        print("AI goes first!")
        human = 'O'
        pc = 'X'
    start = 1 if toss else -1
    while game.game_over(human, pc):
        if start == 1:
            human_move(game,human)
            check(game,human,pc)
            
            pc_move(game,ai,human,pc)            
            check(game,human,pc)
        else:
            pc_move(game,ai,human,pc)
            check(game,human,pc)
            
            human_move(game,human)
            check(game,human,pc)
            
    return render_template('play.html', board=game.board)

def human_move(game,human):
    move=request.form['move']
    row=move//3
    col=move%3
    game.board[row][col]=human
    
def pc_move(game,ai,human,pc):
    _, (row, col) = ai.minimax(3, float('-inf'), float('inf'), True, human, pc)
    game.board[row][col] = pc
    

def check(game,human,pc):
    if game.game_over(human, pc):
        return render_template('result.html', winner=game.evaluate(human, pc))

if __name__ == "__main__":
    app.run(debug=True)






# old code


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



# next steps:

from flask import Flask, render_template, request
import random

app = Flask(__name__)


class TicTacToe:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.number = [[i + j*3 for i in range(3)] for j in range(3)]

    @staticmethod
    def print_board(self):
        for row in self.board:
            print('|'.join(row))
            print('-' * 5)

    def check_winner(self, player):
        for row in self.board:
            if all(cell == player for cell in row):
                return True
        for col in range(3):
            if all(self.board[row][col] == player for row in range(3)):
                return True
        if all(self.board[i][i] == player for i in range(3)) or all(self.board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def game_over(self, human, pc):
        return self.check_winner(human) or self.check_winner(pc) or \
            all(self.board[row][col] != ' ' for row in range(3)
                for col in range(3))

    def evaluate(self, human, pc):
        if self.check_winner(human):
            return 1
        elif self.check_winner(pc):
            return -1
        else:
            return 0

    def empty_cells(self):
        return [(row, col) for row in range(3) for col in range(3) if self.board[row][col] == ' ']

    def empty_board(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]


class TicTacToeAI:
    def __init__(self, game):
        self.game = game

    def minimax(self, depth, alpha, beta, maximizing_player, human, pc):
        if self.game.game_over(human, pc) or depth == 0:
            return self.game.evaluate(human, pc), None

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for row, col in self.game.empty_cells():
                self.game.board[row][col] = 'X'
                eval, _ = self.minimax(
                    depth - 1, alpha, beta, False, human, pc)
                self.game.board[row][col] = ' '
                max_eval = max(max_eval, eval)
                if max_eval >= beta:
                    break
                if max_eval > alpha:
                    alpha = max_eval
                    best_move = (row, col)
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for row, col in self.game.empty_cells():
                self.game.board[row][col] = 'O'
                eval, _ = self.minimax(depth - 1, alpha, beta, True, human, pc)
                self.game.board[row][col] = ' '
                min_eval = min(min_eval, eval)
                if min_eval <= alpha:
                    break
                if min_eval < beta:
                    beta = min_eval
                    best_move = (row, col)
            return min_eval, best_move  

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/play', methods=['POST', 'GET'])
def play():
    game = TicTacToe()
    ai = TicTacToeAI(game)
    toss = random.choice(
            [False, True, True, False, True, False, False, False, True, True, False, True])
    if toss == True:
        print("You go first!")
        human = 'X'
        pc = 'O'
    else:
        print("AI goes first!")
        human = 'O'
        pc = 'X'
    start = 1 if toss else -1
    while game.game_over(human, pc):
        if start == 1:
            human_move(game,human)
            check(game,human,pc)
            
            pc_move(game,ai,human,pc)            
            check(game,human,pc)
        else:
            pc_move(game,ai,human,pc)
            check(game,human,pc)
            
            human_move(game,human)
            check(game,human,pc)
            
    return render_template('play.html', board=game.board,number=game.number)

def human_move(game,human):
    move=request.form['move']
    row=move//3
    col=move%3
    game.board[row][col]=human
    
def pc_move(game,ai,human,pc):
    _, (row, col) = ai.minimax(3, float('-inf'), float('inf'), True, human, pc)
    game.board[row][col] = pc
    

def check(game,human,pc):
    if game.game_over(human, pc):
        return render_template('result.html', winner=game.evaluate(human, pc))

if __name__ == "__main__":
    app.run(debug=True)