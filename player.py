import random
from board import MyBoard
 
class MyPlayer:
    '''Player finds the best weighted score'''
 
    def __init__(self, my_color, opponent_color):
        self.name = 'skulaali'
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
 
        # choosing 1 poss. move and find best opponent's move in next round
        for index_move, move in enumerate(all_possible_moves):
            my_score = my_board.scores[index_move]
 
            # now let's find all possible moves for our opponent...
            opponent_board = MyBoard(self.copy_board(board), my_color=self.opponent_color, opponent_color=self.my_color)
            opponent_board.make_flips(move[0], move[1], possible_directions[index_move])
            opponent_moves = opponent_board.get_possible_moves()
 
            if not(opponent_moves):
                continue
             
            # ...and weight theese moves scores
            opponent_board.find_weighted_scores(opponent_moves)
 
            # but our opponent is also searching for the best move (using the same algorithm)
            for index_my_move, my_move in enumerate(opponent_moves):
                opponent_score = opponent_board.scores[index_my_move]
                my_second_board = MyBoard(self.copy_board(opponent_board.play_board), my_color=self.my_color, opponent_color=self.opponent_color)
                my_second_board.make_flips(my_move[0], my_move[1], opponent_board.possible_directions[index_my_move])
                my_second_board_moves = my_second_board.get_possible_moves()
 
                if not(my_second_board_moves):
                    continue
                 
                my_second_board.find_weighted_scores(my_second_board_moves)
                my_max_score = max(my_second_board.scores)
                opponent_board.scores[index_my_move] = opponent_score - my_max_score
 
            max_opponent_score = max(opponent_board.scores)
            # our total score score in each round is (my move score) - (best opponent score in next round)
            my_board.scores[index_move] = my_score - max_opponent_score
 
 
        max_score = float('-inf') # let's set impossible negative score
        max_items_index_list = list()
 
        # now find the max score (or even scores) indexes 
        # (the index of each score is the same as the index of move that's getting that score)
        for index in range(0, len(my_board.scores)):
            if my_board.scores[index] > max_score:
                max_items_index_list = list()
                max_items_index_list.append(index)
                max_score = my_board.scores[index]
            elif my_board.scores[index] == max_score:
                max_items_index_list.append(index)
 
        # if there is more than 1 max scores, choose index randomly (among best scores)
        if len(max_items_index_list) > 1:
            index = random.choice(max_items_index_list)
            result = (all_possible_moves[index][0], all_possible_moves[index][1])
            return result
         
        index = max_items_index_list[0]
        result = (all_possible_moves[index][0], all_possible_moves[index][1])
 
        # self.scores = list() # clear the array so it will be empty in the next round
        return result
 
    def copy_board(self, board):
        # copy play board so we will not have problems with changing it
        board_copy = list()
        for row in board:
            board_copy.append(row.copy())
 
        return board_copy