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