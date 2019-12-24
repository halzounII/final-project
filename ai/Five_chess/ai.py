import config
from open26 import openings
from board import matrix, board, playersScore
from negamax import deepAll
from opening import match as opening
from score import players as P
class AI:
    def start(self, random = None): # omit 26 kinds of openings
        if random: 
            board.board = openings.random_pick()  # self.???yue
            return {'board': board, 'name': board.board.name}
        return {'board': board}
    def begin(self):  #電腦下棋，開始搜索
        if len(board.allSteps) == 2: p = opening(board) #用開局庫
        else: p = deepAll(None, config.searchDeep)  #遞迴
        board.put(p, P.com)
        return p

    def turn(self, x, y): #下子並計算
        board.put(playersScore(x, y), P.hum)
        return self.begin()
    #delete set
    def forward(self): 
        board.forward()
        
test = AI()
print(test.begin)