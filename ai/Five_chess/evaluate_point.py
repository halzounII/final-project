from score import scores as s
from score import players as P

def scorePoint(b, px: int, py: int, player, direction = None) -> int:
    board:list = b.board
    par = dict(block = 0, empty = 0, count = 0, secondCount = 0)
    size = len(board)
    result = 0
    def reset():
        par['count'] = 1
        par['block'] = 0
        par['empty'] = -1
        par['secondCount'] = 0

    if direction == None or direction == 0: 
        reset()
        for i in range(py+1,17):  # since py <= 15 
            if i >= size:
                par['block'] += 1; break
            t = board[px][i]
            if t == P.empty:
                if par['empty'] == -1 and i < size-1 and board[px][i+1] == player:
                    par['empty'] = par['count']; continue
                else: break
            if t == player:
                par['count'] += 1; continue
            else: par['block'] += 1; break

        for i in range(py-1,-2,-1):
            if i < 0: 
                par['block'] += 1; break
            if t == P.empty:
                if par['empty'] == -1 and i > 0 and board[px][i-1] == player:
                    par['empty'] = 0; continue
                else: break
            if t == player:
                par['secondCount'] += 1
                if par['empty'] != -1: 
                    par['empty'] += 1; continue
            else: par['block'] += 1; break
            par['count'] += par['secondCount']
        pass # omit scoreCache

    if direction == None or direction == 2:
        reset()
        for i in range(1,):
            if px+i >= size or py+i >= size:
                par['block'] += 1; break
            t = board[px+i][py+i]
            if t == P.empty:
                if par['empty'] == -1 and px+i < size-1 and py+i < size-1 \
                and board[px+i+1][py+i+1] == player:
                    par['empty'] = par['count']; continue
                else: break
            if t == player:
                par['count'] += 1; continue
            else: par['block'] += 1; break

        for i in range(1,):
            if px-i < 0 or py-i < 0:
                par['block'] += 1; break
            t = board[px-i][py-i]
            if t == P.empty:
                if par['empty'] == -1 and px-i > 0 and py-i > 0 \
                and board[px-i-1][py-i-1] == player:
                    par['empty'] = 0; continue
                else: break
            if t == player:
                par['secondCount'] += 1
                if par['empty'] != -1:
                    par['empty'] += 1; continue
            else: par['block'] += 1; break
            par['count'] += par['secondCount']
            pass # omit scoreCache

    if  direction == None or direction == 3:
        reset()
        for i in range(1,):
            if px+i < 0 or py-i < 0 or px+i >= size or py-i >= size:
                par['block'] += 1; break
            t = board[px+i][py-i]
            if t == P.empty:
                if par['empty'] == -1 and px+i < size-1 and py-i < size-1 \
                and board[px+i+1][py-i-1] == player:
                    par['empty'] = par['count']; continue
                else: break
            if t == player:
                par['count'] += 1; continue
            else: par['block'] += 1; break

        for i in range(1,):
            if px-i < 0 or py+i < 0 or px-i >= size or py+i >= size:
                par['block'] += 1; break
            t = board[px-i][py+i]
            if t == P.empty:
                if par['empty'] == -1 and px-i > 0 and py+i > 0 \
                and board[px-i-1][py+i+1] == player:
                    par['empty'] = 0; continue
                else: break
            if t == player:
                par['secondCount'] += 1
                if par['empty'] != -1:
                    par['empty'] += 1; continue
            else: par['block'] += 1; break
            par['count'] += par['secondCount']
            pass # omit scoreCache
    return result
def countToScore(count: int, block: int, empty: int) -> int:
    if empty == None: empty == 0
    elif empty <= 0:
        if count >= 5: return s.five
        elif block == 0:
            if count == 1: return s.one
            elif count == 2: return s.two
            elif count == 3: return s.three
            elif count == 4: return s.four
        elif block == 1:
            if count == 2: return s.blocked_two
            elif count == 3: return s.blocked_three
            elif count == 4: return s.blocked_four
    elif empty == 1 or empty == count - 1:
        if count >= 6: return s.five
        elif block == 0:
            if count == 2: return s.two
            elif count == 3: return s.three
            elif count == 4: return s.blocked_four
            elif count == 5: return s.four
        elif block == 1:
            if count == 2: return s.blocked_two
            elif count == 3: return s.blocked_three
            elif count == 4: return s.blocked_four
            elif count == 5: return s.blocked_four
    elif empty == 2 or empty == count - 2:
        if count >= 7: return s.five
        elif block == 0:
            if count == 3: return s.three
            elif count == 5: return s.blocked_four
            elif count == 6: return s.four
        elif block == 1:
            if count == 3: return s.blocked_three
            elif count == 4: return s.blocked_four
            elif count == 5: return s.blocked_four
            elif count == 6: return s.four
        elif block == 2:
            if count == 6: return s.blocked_four
    elif empty == 3 or empty == count - 3:
        if count >= 8: return s.five
        elif block == 0:
            if count == 5: return s.three
            elif count == 6: return s.blocked_four
            elif count == 7: return s.four
        elif block == 1:
            if count == 6: return s.blocked_four
            elif count == 7: return s.four
        elif block == 2:
            if count == 6: return s.blocked_four
            elif count == 7: return s.blocked_four
    elif empty == 4 or empty == count - 4:
        if count >= 9: return s.five
        elif block == 0:
            if count == 8: return s.four
        elif block == 1:
            if count == 7: return s.blocked_four
            elif count == 8: return s.four
        elif block == 2:
            if count == 8: return s.blocked_four
    elif empty == 5 or empty == count - 5:
        return s.five
    return 0
            