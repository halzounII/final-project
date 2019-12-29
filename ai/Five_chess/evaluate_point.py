from score import scores as s
from score import players as P

# TO DO:
    # 1. dir = 2 or 3 的 range() 參數
def scorePoint(b, px: int, py: int, player: int, direction = None) -> int:
    board: list = b.board
    par = dict(block = 0, empty = 0, count = 0, secondCount = 0)
    size = b.size
    result = 0
    def reset():
        par['count'] = 1  #表示該方向上有幾顆不被對方棋子隔開的己方棋子(包含該顆棋子)
        par['block'] = 0  #表示有對方棋子或到棋盤邊
        par['empty'] = -1 #表示在第幾顆棋子後(包含該顆棋子)有空格
        par['secondCount'] = 0  #反方向的count

    if (not direction) or direction == 0: 
        reset()
        # 橫排向右是否有棋
        for i in range(py+1,17):  # since py <= 15 
            if i >= size:
                par['block'] += 1; break #超出棋盤，加block，跳出
            t = board[px][i]
            if t == P.empty :
                if par['empty'] == -1 and i + 1 < size and board[px][i+1] == player:
                    par['empty'] = par['count']; continue  #若從該顆棋子到此還沒有其他對手棋子或空格
                #且下一顆是己方棋子，則empty = count
                else: break            #超過一個空格，或下一個是對手棋子，跳出 
            elif t == player:
                par['count'] += 1           #有己方棋，加count
            else: par['block'] += 1; break  #有對手棋，加block，跳出
         #橫排向左是否有棋
        for i in range(py-1,-2,-1):
            if i < 0: 
                par['block'] += 1; break #超出棋盤，加block
            if t == P.empty:
                if par['empty'] == -1 and i > 0 and board[px][i-1] == player:
                    par['empty'] = 0; continue  #??
                else: break
            if t == player:
                par['secondCount'] += 1      #有己方棋，加count
                if par['empty'] != -1:       #??
                    par['empty'] += 1; continue
            else: par['block'] += 1; break   #有對手棋，加block
            par['count'] += par['secondCount']
        pass # omit scoreCache
        par['count'] += par['secondCount']
        b.scoreCache[player][0][px][py] = countToScore(par['count'], par['block'], par['empty'])
    result += b.scoreCache[player][0][px][py] # 把分數儲存在scoreCache裡

    if (not direction) or direction == 0: 
        reset()
        # 直行向上是否有棋
        for i in range(px+1,17):  # since px <= 15 
            if i >= size:
                par['block'] += 1; break #超出棋盤，加block
            t = board[i][py]
            if t == P.empty :
                if par['empty'] == -1 and i + 1 < size and board[i+1][py] == player:
                    par['empty'] = par['count']; continue  #??
                else: break
            elif t == player:
                par['count'] += 1           #有己方棋，加count
            else: par['block'] += 1; break  #有對手棋，加block
         #直行向下是否有棋
        for i in range(px-1,-2,-1):
            if i < 0: 
                par['block'] += 1; break #超出棋盤，加block
            if t == P.empty:
                if par['empty'] == -1 and i > 0 and board[i-1][py] == player:
                    par['empty'] = 0; continue  #??
                else: break
            if t == player:
                par['secondCount'] += 1      #有己方棋，加count
                if par['empty'] != -1:       #??
                    par['empty'] += 1; continue
            else: par['block'] += 1; break   #有對手棋，加block
            par['count'] += par['secondCount']
        pass # omit scoreCache
        par['count'] += par['secondCount']
        b.scoreCache[player][1][px][py] = countToScore(par['count'], par['block'], par['empty'])
    result += b.scoreCache[player][1][px][py]

    if (not direction) or direction == 2:
        reset()
        #右下是否有棋
        for i in range(1,):   #unfinished
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
        #左上是否有棋
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
        par['count'] += par['secondCount']
        b.scoreCache[player][2][px][py] = countToScore(par['count'], par['block'], par['empty'])
    result += b.scoreCache[player][2][px][py]

    if  (not direction) or direction == 3:
        reset()
        #右上是否有棋
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
        #左下是否有棋
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
        par['count'] += par['secondCount']
        b.scoreCache[player][3][px][py] = countToScore(par['count'], par['block'], par['empty'])
    result += b.scoreCache[player][3][px][py]
    return result
#為每一種棋型評分
def countToScore(count: int, block: int, empty: int = 0) -> int:
    if empty <= 0:
        if count >= 5: return s.five #沒空格有五顆，連五
        elif block == 0:             #沒block(或許反方向第一顆是?)
            if count == 1: return s.one
            elif count == 2: return s.two
            elif count == 3: return s.three
            elif count == 4: return s.four
        elif block == 1: # omit block_one
            if count == 2: return s.blocked_two
            elif count == 3: return s.blocked_three
            elif count == 4: return s.blocked_four
    elif empty == 1 or empty == count - 1:  #最後一子前方有空格
        if count >= 6: return s.five        # 5 + blank + 1
        elif block == 0:
            if count == 2: return s.two/2   # 間二
            elif count == 3: return s.three
            elif count == 4: return s.blocked_four
            elif count == 5: return s.four
        elif block == 1:
            if count == 2: return s.blocked_two
            elif count == 3: return s.blocked_three
            elif count == 4: return s.blocked_four
            elif count == 5: return s.blocked_four
    elif empty == 2 or empty == count - 2:   #倒數第二子前方有空格
        if count >= 7: return s.five       # 5 + blank + 2
        elif block == 0:                   # 評分需要修正
            if count == 3: return s.blocked_three
            elif count == 4: return s.three
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