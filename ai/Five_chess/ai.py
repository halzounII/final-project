import config
from open26 import openings
from board import matrix, board, playersScore
from negamax import deepAll
from opening import match as opening
from score import players as P
from evaluate_point import scorePoint
class AI:
    def start(self, random = None): # omit 26 kinds of openings
        if random: 
            board.board = openings.random_pick()  # self.???yue
            return {'board': board, 'name': board.board.name}
        return {'board': board}
    def begin(self):  #電腦下棋，開始搜索
        if board.allSteps == []: p = playersScore(7,7) 
        #elif len(board.allSteps) == 2: 
            #x, y = opening(board)[0], opening(board)[1] #用開局庫
            #p = playersScore(x, y)
        else: p = deepAll(deep = config.searchDeep)  #遞迴
        if board.board[p.pos[0]][p.pos[1]] == P.empty:
            board.put(P.com, p)
            board.initScore()  #重新評估局面情勢
            print(board)
            return p
        else: return

    def backward(self):
        board.backward()

    def forward(self): 
        board.forward()
ai = AI()

if __name__ == '__main__':
    if input('who first?') == '1': ai.begin()
    print(board)
    while True:
        #bk = input('bk')
        #if bk == 'bk': ai.backward()
        #elif bk == 'fk': ai.forward()
        if True:
            x,y = int(input('x:')), int(input('y:'))
            if board.board[x][y] == P.empty: 
                board.put(P.hum, playersScore(x, y))
                board.stepsTail = []
                print(ai.begin().pos)
                
        print(board)
        table, table2 = '', ''
        for i in range(15):
            table += ''.join(str(board.humScore[i])) + '\n'
            table2 += ''.join(str(board.comScore[i])) + '\n'
        #print(board.currentSteps)
        #print(board.allSteps)
        #print(board.allSteps)
        print(table)
        print(table2)
        if input() == '':
            config.eval_point = True
            print(scorePoint(board, int(input('x:')), int(input('y:')), int(input('player:'))))  #debug用
            print(scorePoint(board, int(input('x:')), int(input('y:')), int(input('player:'))))  #debug用
            config.eval_point = False
