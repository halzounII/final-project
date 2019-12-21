from score import players as P
from board import board, playersScore
import config
from negamax import deepAll
from opening import match as opening
class AI:
    #def start(self): # omit 26 kinds of openings
        #return board
    def begin(self):  #電腦下棋，開始搜索
        if 1 <= len(board.allSteps) <= 2: p = opening(board) #用開局庫
        else: p = deepAll(None, config.searchDeep)  #遞迴
        board.put(p, P.com)
        return p

    def turn(self, x, y): #下子並計算
        board.put(playersScore(x, y), P.hum)
        return self.begin()
    #delete set
    def forward(self): 
        board.forward()