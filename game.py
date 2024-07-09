from board import MyBoard
from minmax_player import MinimaxPlayer
from greedy_player import GreedyPlayer

INITIAL_BOARD = [
    [-1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, 0, 1, -1, -1, -1],
    [-1, -1, -1, 1, 0, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1],
]


def copy_board(board):
    # copy play board so we will not have problems with changing it
    board_copy = list()
    for row in board:
        board_copy.append(row.copy())
    return board_copy

def is_still_on_board(x, y):
        # checking if coordinates are valid
 
        x_on_board = x >= 0 and x < 8
        y_on_board = y >= 0 and y < 8
         
        return x_on_board and y_on_board

def flip_pieces(board, x, y, player):
    opponent = 1 if player == 0 else 0
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if not(is_still_on_board(nx, ny)) or board[nx][ny] == -1 or board[nx][ny] == player:
            continue

        pieces_to_flip = []
        while is_still_on_board(nx, ny) and board[nx][ny] == opponent:
            pieces_to_flip.append((nx, ny))
            nx += dx
            ny += dy

            if is_still_on_board(nx, ny) and board[nx][ny] == player:
                for fx, fy in pieces_to_flip:
                    board[fx][fy] = player

    return board
                
# Greedy plays first
def greedy_first(player1, player2):
    round_count = 0
    SCORE_GREEDY = 0
    SCORE_MINIMAX = 0
    board = copy_board(INITIAL_BOARD)
    game_running = True
    #TODO kod hujnya need to rewrite so parameters can be switched
    while game_running:
        res1 = player1.move(board)
        if res1 == None:
            game_running = False
            continue
        xG, yG = res1
        board[xG][yG] = 1
        board = flip_pieces(board, xG, yG, 1)

        res2 = player2.move(board)
        if res2 == None:
            game_running = False
            continue

        #print_board(board)
        #print()
        xM, yM = res2
        board[xM][yM] = 0
        board = flip_pieces(board, xM, yM, 0)

        round_count += 1
        #print_board(board)

    
    for x in board:
        SCORE_GREEDY += x.count(1)
        SCORE_MINIMAX += x.count(0)

    print("G: ", SCORE_GREEDY, "M: ", SCORE_MINIMAX)
    print_board(board)

    return (SCORE_GREEDY, SCORE_MINIMAX)
        


def main():
    minmax_player = MinimaxPlayer(0, 1)  # 0 for Minimax
    greedy_player = GreedyPlayer(1, 0)   # 1 for Greedy

    results = []
    for x in range(100):
        res = greedy_first(greedy_player, minmax_player)
        results.append(res)
        print("Game #", x, "ended")

    return results
    

def print_board(board):
    for row in range(8):
        for col in range(8):
            print(str(board[row][col]) + " ", end=" ")
        print("\n")
    print("--------------------------------")

if __name__ == "__main__":
    main()
