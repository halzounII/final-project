from score import players as P
from board import Board
import config 
from negamax import deepAll
board = Board(15)
class AI:
    #def start(self): # omit 26 kinds of openings
        #board = Board(15)
        #return board
    def begin(self):
        if len(board.allSteps) > 1: p = opening(board)
        else: p = deepAll(None, config.searchDeep)
        board.put(p, P.com)
        return p
    def turn(self, x, y):
        self.Set(x, y, P.hum)
        return self.begin
    def Set(self, x, y, r) -> None: 
        board.put((x,y), r)
    def forward(self): 
        board.forward()