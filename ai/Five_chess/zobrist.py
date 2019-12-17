from score import players as P
from random import random

class Zobrist:
    def __init__(self):
        self.length = 15
        self.com = []
        self.hum = []
        for i in range(self.length**2):
            self.com.append(self._rand())
            self.hum.append(self._rand())
        self.code = self._rand()
    def _rand(self):
        return round(random()*(10**9)) 
    def go(self, x, y, player):
        i = self.length*x + y
        if player == P.com: self.code = self.code ^ self.com[i]
        else: self.code = self.code ^ self.hum[i]
        return self.code
z = Zobrist()