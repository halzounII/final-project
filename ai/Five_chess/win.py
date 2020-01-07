from score import players as P
from board import board, playersScore

def Fives(board, player, place = playersScore())-> int:
    count = 1
    for i in range(place.pos[1] + 1, board.size):
        if board.board[place.pos[0]][i] != player: break
        count += 1
    for i in range(place.pos[1] - 1, -1 , -1):
        if board.board[place.pos[0]][i] != player: break
        count += 1
    if count >= 5: return 1
    
    count = 1
    for i in range(place.pos[0] + 1, board.size):
        if board.board[i][place.pos[1]] != player: print(count); break
        count += 1
    for i in range(place.pos[0] - 1, -1 , -1):
        if board.board[i][place.pos[1]] != player: break
        count += 1
    if count >= 5: return 2

    # need modifying
    count = 1
    for i in range(1, board.size):
        if place.pos[0] + i >= board.size or place.pos[1] + i >= board.size\
            or board.board[place.pos[0] + i][place.pos[1] + i] != player: break
        count += 1
    for i in range(-1, -1 , -1):
        if place.pos[0] + i <= 0 or place.pos[1] + i <= 0\
            or board.board[place.pos[0] + i][place.pos[1] + i] != player: break
        count += 1
    if count >= 5: return 3

    count = 1
    for i in range(1, board.size):
        if place.pos[0] + i >= board.size or place.pos[1] - i <= 0\
            or board.board[place.pos[0] + i][place.pos[1] - i] != player: break
        count += 1
    for i in range(-1, -1 , -1):
        if place.pos[0] + i <= 0 or place.pos[1] - i >= board.size\
            or board.board[place.pos[0] + i][place.pos[1] - i] != player: break
        count += 1
    if count >= 5: return 4
    return 0

def w(board):
    d = 0
    for i in range(board.size):
            for j in range(len(board.board[i])):
                if i != d and j != d:
                    t = board.board[i][j]
                    place = playersScore(i, j)
                    if t != P.empty:
                        d = Fives(board, t, place)
                        if d : break
    if not d or d == 0: return False
    if d == 1: return [place.pos] + [[place.pos[0], place.pos[1] + i] for i in range(1, 5)]
    if d == 2: return [place.pos] + [[place.pos[0] + i, place.pos[1]] for i in range(1, 5)]
    if d == 3: return [place.pos] + [[place.pos[0] + i, place.pos[1] + i] for i in range(1, 5)]
    if d == 4: return [place.pos] + [[place.pos[0] + i, place.pos[1] - i] for i in range(1, 5)]