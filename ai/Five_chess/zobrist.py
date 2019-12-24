from random import random
from score import players as P

class Zobrist:
    def __init__(self):
        self.length = 15
        self.com = []
        self.hum = []
        for i in range(self.length**2): #為棋盤上每個點產生亂數
            self.com.append(self._rand())
            self.hum.append(self._rand())
        self.code = self._rand()
    def _rand(self):
        return round(random()*(10**9)) 
    def go(self, x, y, player):        #執行zobrist運算
        i = self.length*x + y          #該點在list裡的位置
        if player == P.com: self.code = self.code ^ self.com[i]  #目前的code XOR 那一點的亂碼
        else: self.code = self.code ^ self.hum[i]
        return self.code
z = Zobrist()