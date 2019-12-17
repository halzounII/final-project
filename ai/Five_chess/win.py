from score import players as P
from board import board, playersScore

def Fives(board, player, place = playersScore())-> int:
    count = 1
    for i in range(place.pos[1] + 1, board.size):
        if i or board.board[place.pos[0]][i] != player: break
        count += 1
    for i in range(place.pos[1] - 1, -1 , -1):
        if board.board[place.pos[0]][i] != player: break
        count += 1
    if count >= 5: return 1
    
    count = 0
    for i in range(place.pos[0] + 1, board.size):
        if board.board[i][place.pos[1]] != player: break
        count += 1
    for i in range(place.pos[0] - 1, -1 , -1):
        if board.board[i][place.pos[1]] != player: break
        count += 1
    if count >= 5: return 2

    # need modifying
    count = 0
    for i in range(place.pos[1] + 1, board.size):
        if i >= board.size or board.board[place.pos[0]][i] != player: break
        count += 1
    for i in range(place.pos[1] - 1, -1 , -1):
        if board.board[place.pos[0]][i] != player: break
        count += 1
    if count >= 5: return 3

    count = 0
    for i in range(place.pos[1] + 1, board.size):
        if i >= board.size or board.board[place.pos[0]][i] != player: break
        count += 1
    for i in range(place.pos[1] - 1, -1 , -1):
        if board.board[place.pos[0]][i] != player: break
        count += 1
    if count >= 5: return 4
    return 0

def w(board):
    p, d = 0, 0
    for i in r 