#!/usr/bin/env python
# coding: utf-8

from score import scores as s
from score import players as P
from evaluate_point import scorePoint 
from collections import deque
from zobrist import z
import config
# ToDo:
#   1. add starTo to board
#   2. modify place - done
#   3. self.v initialization
def matrix(size: int = 15) -> list:
    return [[0 for i in range(size)] for j in range(size)]

def fixScore(Type: int) -> int: # 避免無謂衝四
    if s.blocked_four <= Type < s.four:
        if s.blocked_four <= Type < (s.blocked_four + s.three): return s.three     # 單死四
        elif (s.blocked_four + s.three) <= Type < s.blocked_four*2: return s.four  # 死四活三
        else: return s.four*2  # 雙死四
    return Type

def starTO (point: tuple, points: list) -> bool:
    if not (points and len(points)): return False
    a = point
    for i in range(len(points)):
        b = points[i]
        if abs(a[0]-b[0]) > 4 and abs(a[1]-b[1]) > 4: return False
        if not (a[0] == b[0]) or a[1] == b[1] or abs(a[0]-b[0]) == abs(a[1]-b[1]): return False
    return True

class playersScore:        # new class
    def __init__(self, i=0, j=0) -> dict:
        self.pos = [i,j]
        self.score: int = 0   #該位置的最大可能得分
        self.scoreCom: int = 0 #AI在該位置的得分
        self.scoreHum: int = 0 #人類在該位置的得分
        self.player: int = 0  
        self.v = dict()    #used in negamax.negamax
    def __lt__(self, other):
        return abs(self.score) < abs(other.score)    # used in vcx.py (result.sort())
        
class Board:
    def __init__(self, size: int = 15) -> None:
        self.evaluateCache = {}   # redundant?
        self.currentSteps = []    #當前的那一步，元素是playersScore()
        self.allSteps = []   # all chess pieces put by both sides, 元素是playersScore(), used in ai.py
        self.stepsTail = []  #backward(悔棋)後保留的先前棋步
        self._last = [False,False]
        self.count = 0       #手數
        self.z = z
        if size:       # accept only integer, not lists
            self.board = matrix(size)             #目前棋盤的落子狀況;元素是score.players()
            self.size = size                      #棋盤大小
            self.comScore = matrix(size)          #AI在棋盤某一位置的(可能)得分;元素是數字
            self.humScore = matrix(size)          #人類在棋盤某一位置的(可能)得分;元素是數字
            self.scoreCache = [                   # used in evalueate-point.py                 
                [],   # placeholder
                [matrix(size) for i in range(4)],  # for player 1 
                [matrix(size) for j in range(4)]]  # for player 2  
        self.initScore()

    def __str__(self):
        if self.size >= 0:
            table = ''
            for i in range(self.size):
                table += ''.join(str(self.board[i])) + '\n'
            return table
    #檢查在以該格為中心，邊長 = 2distance + 1 的矩形內是否有至少 count 個棋子
    def hasNeighbor(self, x: int, y: int, distance: int = 1, count: int = 1) -> bool:
        for i in range(x-distance, x+distance + 1):
            if i < 0 or i >= self.size: continue
            for j in range( y-distance, y+distance + 1):
                if j < 0 or j >= self.size: continue
                elif (i, j) == (x, y): continue
                elif self.board != P.empty:
                    count -= 1
                    if count <= 0 : return True
        return False

    # score for a certain loc for a certain player
    def initScore(self) -> None:                      #初始化每一格的分數  
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == P.empty:   
                    if self.hasNeighbor(i, j, 2, 2):  
                    #5*5內有2顆棋子以上的空格，計算在該格落子後可得的分數
                        self.comScore[i][j] = scorePoint(self, i, j, P.com)
                        self.humScore[i][j] = scorePoint(self, i, j ,P.hum)
                elif self.board[i][j] == P.com:
                    self.comScore[i][j] = scorePoint(self, i ,j, P.com)
                    self.humScore[i][j] = 0             #該格為電腦棋，則玩家得分0
                elif self.board[i][j] == P.hum:
                    self.humScore[i][j] = scorePoint(self, i ,j, P.hum)
                    self.comScore[i][j] = 0

    def updateScore(self, place = playersScore()) -> None:     # p => place # 米字形更新分數
        radius = 4                     #更新的距離半徑(遠於五格者不受影響)
        def update(x, y, direction):
            player = self.board[x][y]
            if player != P.reverse(P.com):
                self.comScore[x][y] = scorePoint(self, x, y, P.com, direction)
                pass #statistics
            else: self.comScore[x][y] = 0
            if player != P.reverse(P.hum):
                self.humScore[x][y] = scorePoint(self, x, y, P.hum, direction)
                pass #statistics
            else: self.humScore[x][y] = 0
        pass # optimization(optional)
        for i in range(-radius, radius+1):
            #橫排更新
            if place.pos[1] + i < 0: continue     #超出邊界但才剛開始遞迴，跳過
            if place.pos[1] + i >= self.size : break  #超出邊界，跳出
            update(place.pos[0], place.pos[1] + i, 0)
            #直行更新
        for i in range(-radius, radius+1):
            if place.pos[0] + i < 0: continue
            if place.pos[0] + i >= self.size: break
            update(place.pos[0] + i, place.pos[1], 1)
            #右下左上更新
        for i in range(-radius, radius+1):
            if place.pos[0] + i < 0 or place.pos[1] + i < 0: continue
            if place.pos[0] + i >= self.size or place.pos[1] + i >= self.size: break
            update(place.pos[0] + i, place.pos[1] + i, 2)
            #右上左下更新
        for i in range(-radius, radius+1):
            if place.pos[0] + i < 0 or place.pos[1] - i >= self.size: continue
            if place.pos[0] + i >= self.size or place.pos[1] - i < 0: break # or continue?-solved
            update(place.pos[0] + i, place.pos[1] - i, 3)

    
    def put(self, player: int, place = playersScore()) -> None:
        if self.board[place.pos[0]][place.pos[1]] != 0: return  #該位置已經有棋
        if player == 0: player = 2 #遇到bug
        if config.debug: print(f'put[{place.pos}] {player}')
        self.board[place.pos[0]][place.pos[1]] = player
        self.z.go(place.pos[0], place.pos[1], player) #執行zobrist運算，產生棋型代碼
        self.allSteps.append(place)   #把此步加到所有步數裡
        self.currentSteps.append(place)
        #self.stepsTail = []  #棋局往另一方向發展，不再保留先前棋步
        self.updateScore(place)
        self.count += 1
        #print(f'put {place.pos},{player}, {self.currentSteps}')

    def remove(self, place = playersScore()) -> None:
        if self.board[place.pos[0]][place.pos[1]] == 0: return  #該位置沒棋
        self.z.go(place.pos[0], place.pos[1], self.board[place.pos[0]][place.pos[1]])
        if config.debug: print(f'remove{place.pos} {place.player}')
        self.updateScore(place)
        self.allSteps.pop()
        if self.currentSteps != []: self.currentSteps.pop()
        self.board[place.pos[0]][place.pos[1]] = P.empty
        self.count -= 1

    def backward(self):
        if len(self.allSteps) < 2: return
        for i in range(2):
            s = self.allSteps[-1]
            self.stepsTail.append(s)
            self.remove(s)

    def forward(self):
        if len(self.stepsTail) < 2: return
        for i in range(2):
            s = self.stepsTail.pop()
            self.put(s.player, s)

    def evaluate(self, player: int) -> int:  # 當前各自修正後的分數差距
        self.comMaxScore, self.humMaxScore = 0, 0
        for i in range(self.size):
            for j in range(self.size):  # board[i]??
                if self.board[i][j] == P.com:
                    self.comMaxScore += fixScore(self.comScore[i][j])
                elif self.board[i][j] == P.hum:
                    self.humMaxScore += fixScore(self.humScore[i][j])
        return (1 if player == P.com else -1)*(self.comMaxScore - self.humMaxScore)
    # starspread: 米字計算
    # generator: 回傳所有可能的應手，以五->三排列
    def generator(self, player: int, onlyThrees, starSpread) -> list:
        #print('player is ' + str(player)) --debug
        if self.count <= 0: return [7,7] #棋局還沒開始
        fives = []
        com_fours = []; hum_fours = []
        com_blockedfours = []; hum_blockedfours = []
        com_doublethrees = []; hum_doublethrees = []
        com_threes = []; hum_threes = []
        com_twos = deque(); hum_twos = deque()
        neighbors = []
        attackPoints = []
        defendPoints = []
        if starSpread and config.star: # config.py
            i = len(self.allSteps) - 1  
            while i >= 0:
                place = self.allSteps[i]  #某一方的棋步
                if (P.reverse(player) == P.com and place.scoreCom >= s.three)\
                    or (P.reverse(player) == P.hum and place.scoreHum >= s.three): 
                    #對方的防守點
                    defendPoints.append(place); break  #表示對方該子在防守
                i -= 2 # 上一步
            j = len(self.allSteps) - 2
            while j >= 0:
                place = self.allSteps[i]
                if (player == P.com and place.scoreCom >= s.three) \
                    or (player == P.hum and place.scoreHum >= s.three):
                    #己方的防守點
                    attackPoints.append(place); break  #表示己方該子在進攻
                j -= 2
            #若沒有進攻/防守點，則設為首步
            if len(self.allSteps) >= 2: #needs debug    
                if not len(attackPoints): 
                    attackPoints.append(self.allSteps[0] if self.allSteps[0].player == player else self.allSteps[1])
                if not len(defendPoints):
                    defendPoints.append(self.allSteps[0] if self.allSteps[0].player == P.reverse(player) else self.allSteps[1])
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == P.empty:
                    if len(self.allSteps) < 6:
                     #總手數小於6(雙方皆不可能成三)，若周圍沒棋就跳過
                        if not self.hasNeighbor(i, j, 1, 1): continue
                    elif not self.hasNeighbor(i, j, 2, 2): continue
                   #5*5內沒棋也跳過(不可能有連棋)
                    place = playersScore(i, j)    # replace p of place
                    place.scoreHum = self.humScore[i][j]
                    place.scoreCom = self.comScore[i][j]
                    place.score = max(place.scoreCom, place.scoreHum)
                    #只看活三以上
                    if onlyThrees and place.score < s.three: continue
                    place.player = player
                    pass # starspread
                    if place.scoreCom >= s.five: fives.append(place)
                    elif place.scoreHum >= s.five: fives.append(place)
                    elif place.scoreCom >= s.four: com_fours.append(place)
                    elif place.scoreHum >= s.four: hum_fours.append(place)
                    elif place.scoreCom >= s.blocked_four: com_blockedfours.append(place)
                    elif place.scoreHum >= s.blocked_four: hum_blockedfours.append(place)
                    elif place.scoreCom >= 2*s.three: com_doublethrees.append(place)
                    elif place.scoreHum >= 2*s.three: hum_doublethrees.append(place)
                    elif place.scoreCom >= s.three: com_threes.append(place)
                    elif place.scoreHum >= s.three: hum_threes.append(place)
                    elif place.scoreCom >= s.two: com_twos.appendleft(place)
                    elif place.scoreHum >= s.two: hum_twos.appendleft(place)
                    else: neighbors.append(place) # 沒有連棋，而周圍有對手棋 
                    
        if len(fives): #print('fives')
            return fives   #有連五，先返回
        elif player == P.com and len(com_fours): #print('com_fours')
            return com_fours  #自己可活四就先活四
        elif player == P.hum and len(hum_fours): #print('hum_fours')
            return hum_fours  #否則防守對方活四
        elif player == P.com and len(hum_fours) and not len(com_blockedfours): #print('def_hum_fours')
            return hum_fours
        elif player == P.hum and len(com_fours) and not len(hum_blockedfours): #print('def_com_fours')
            return com_fours
        #對面有活四，自己有死四
        fours = com_fours + hum_fours if player == P.com else hum_fours + com_fours
        blockedfours = com_blockedfours + hum_blockedfours if player == P.hum else hum_blockedfours + com_blockedfours
        if len(fours): #print('blockedfours')
            return fours + blockedfours 
        #自己的活四點先排前面(這裡理應沒有)，再排對方活四點，再排自己與對方死四點
        if player == P.com:  #先雙三，再死四，再活三
            result = com_doublethrees + hum_doublethrees + com_blockedfours + hum_blockedfours + com_threes + hum_threes
        elif player == P.hum: 
            result = hum_doublethrees + com_doublethrees + hum_blockedfours + com_blockedfours + hum_threes + com_threes           
        if len(com_doublethrees) or len(hum_doublethrees): return result
        elif onlyThrees: return result  #不考慮活二死二的情形
        twos = com_twos + hum_twos if player == P.com else hum_twos + com_twos
        result += twos if len(twos) else neighbors
        #分數低可只計到countLimit
        if len(result) > config.countLimit: return result[:config.countLimit]
        return result  
board = Board()
if __name__ == '__main__':
    while input() == '':
        print(scorePoint(board, int(input('x:')), int(input('y:')), int(input('player:'))))