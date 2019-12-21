# 開局第三手
#def respond(s, pre, res):

def huayue(board):
    s = board.steps  #??
    if len(s) == 2:
        if s[1].pos == [6,7]: return [6,8]
        elif s[1].pos == [7,6]: return [6,6]
        elif s[1].pos == [8,7]: return [8,6]
        elif s[1].pos == [7,8]: return [8,8]

def puyue(board):
    s = board.steps
    if len(s) == 2:
        if s[1].pos == [6,6]: return [6,8]
        elif s[1].pos == [8,6]: return [6,6]
        elif s[1].pos == [8,8]: return [8,6]
        elif s[1].pos == [6,8]: return [8,8]
def match(board):
    #if len(board.allSteps) > 2: return False  雙方已各下一手
    if board.board[board.allSteps[0].pos[0]][board.allSteps[0].pos[1]] != 1:
        return False     # 不是電腦先手
    for i in [[6,7], [7,6], [8,7], [7,8]]:
        if board.allSteps[1].pos == i: return huayue(board)
    for i in [[6,6], [8,8], [6,8], [8,6]]:
        if board.allSteps[1].pos == i: return puyue(board)
    return False