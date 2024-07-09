from board import MyBoard


class GreedyPlayer:
    '''Player choose max score in one round'''
 
    def __init__(self, my_color, opponent_color):
        self.name = 'skulaali' # for school assignment
        self.my_color = my_color
        self.opponent_color = opponent_color        
        self.play_board = None
 
 
    def move(self, board):
        if not (board):
            return None
 
        # read MyBoard description
        my_board = MyBoard(self.copy_board(board), my_color=self.my_color, opponent_color=self.opponent_color)
 
        # let's find all posible moves for my player
        all_possible_moves = my_board.get_possible_moves()
        size_all_possible_moves = len(all_possible_moves)
        possible_directions = my_board.possible_directions
 
        # if all_possible_moves is empty, there is no available moves in this round
        if size_all_possible_moves < 1:
            return None
         
        # find weigthed score for each possible move
        my_board.find_weighted_scores(all_possible_moves)
 
        # find the move with the maximum score
        max_score = float('-inf')
        best_move_index = 0

        for index, score in enumerate(my_board.scores):
            if score > max_score:
                max_score = score
                best_move_index = index

        result = (all_possible_moves[best_move_index][0], all_possible_moves[best_move_index][1])

        return result
  
 
    def copy_board(self, board):
        # copy play board so we will not have problems with changing it
        board_copy = list()
        for row in board:
            board_copy.append(row.copy())
 
        return board_copy