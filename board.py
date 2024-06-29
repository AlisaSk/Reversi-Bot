class MyBoard:
    ''' ## MyBoard
    This class works with board matrix: change it, analize it'''
 
    #  all reversi strategies are based on idea that some squares (positions)
    #  are more valuable than others (i.e. corners or center 2x2)
    #  so i will use weights_matrix which will analize the value of each position
    SQUARE_WEIGHTS = [
    #      0    1    2    3    4    5    6    7
        [120, -20,  20,   5,   5,  20, -20, 120], # 0
        [-20, -40,  -5,  -5,  -5,  -5, -40, -20], # 1
        [ 20,  -5,  15,   3,   3,  15,  -5,  20], # 2
        [  5,  -5,   3,   3,   3,   3,  -5,   5], # 3
        [  5,  -5,   3,   3,   3,   3,  -5,   5], # 4
        [ 20,  -5,  15,   3,   3,  15,  -5,  20], # 5
        [-20, -40,  -5,  -5,  -5,  -5, -40, -20], # 6
        [120, -20,  20,   5,   5,  20, -20, 120], # 7
    ]
     
    def __init__(self, board, my_color, opponent_color):
        self.play_board = board
        self.size_of_board = len(board)
        self.my_color = my_color
        self.opponent_color = opponent_color
 
        self.possible_directions = list()
        self.scores = list()
 
    def make_flips(self, x, y, delta):
        # changing board according to our move
        del_x = delta[0]
        del_y = delta[1]
        while self.is_still_on_board(x, y) and self.play_board[x][y] != self.opponent_color:
            self.play_board[x][y] = self.opponent_color
            x += del_x
            y += del_y
     
 
    def get_possible_moves(self):
        all_moves = list()
 
        # check each square on the board
        for row in range(self.size_of_board):
            for col in range(self.size_of_board):
                if self.is_valid_move(row, col):
                    all_moves.append([row, col])
 
        return all_moves
     
     
    def is_valid_move(self, x, y):
        # check if the square is empty
        if self.play_board[x][y] != -1:
            return False
         
        for step in self.get_steps():
            #let's move in chosen direction
            current_x = x + step[0]
            current_y = y + step[1]
 
            if not(self.is_still_on_board(current_x, current_y)):
                continue
 
            # if opponent is not around empty square, it's impossible move
            if self.play_board[current_x][current_y] != self.opponent_color:
                continue
 
            while self.is_still_on_board(current_x, current_y):
                # if there is any blank spaces, it's impossible move
                if self.play_board[current_x][current_y] == -1:
                    break
                # if there is our peice at the end, it's possible move
                if self.play_board[current_x][current_y] == self.my_color:
                    # saving direction here so each direction will have the same
                    # index as their move
                    self.possible_directions.append([step[0], step[1]])
                    return True
                   
                current_x += step[0]
                current_y += step[1]
 
        return False
 
 
    def get_steps(self):
        steps = list()
 
        # getting all possible directions
        for first in -1, 0, 1:
            for second in -1, 0, 1:
                if first == 0 and second == 0:
                    continue
                steps.append([first, second])
 
        return steps
 
 
    def is_still_on_board(self, x, y):
        # checking if coordinates are valid
        if not self.size_of_board:
            return False
 
        x_on_board = x >= 0 and x < self.size_of_board
        y_on_board = y >= 0 and y < self.size_of_board
         
        return x_on_board and y_on_board
     
 
    def find_weighted_scores(self, moves):
        for index, move in enumerate(moves):
            score = 0
            # set coordinates
            x = move[0]
            y = move[1]
            del_x = self.possible_directions[index][0]
            del_y = self.possible_directions[index][1]
            score = self.set_weights(x, y, del_x, del_y, score)
                 
            self.scores.append(score)   
     
     
    def set_weights(self, x, y, del_x, del_y, score):
        # flipping all pieces and add their scores until find our piece
        while self.is_still_on_board(x, y) and self.play_board[x][y] != self.my_color:
            score += MyBoard.SQUARE_WEIGHTS[x][y]
            x += del_x
            y += del_y
 
        return score
    