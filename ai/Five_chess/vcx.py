import config
from zobrist import z
from board import board, playersScore
from score import scores as s
from score import players as P
from collections import deque
from math import floor
from random import random

class var:
    MAX_SCORE = s.three
    MIN_SCORE = s.four
    checkmate = {'totalCount': 0, 'cacheCount': 0, 'cacheHit': 0}
    Cache = {'VCT':{}, 'VCF': {}}
lastMaxPoint = playersScore()

def maximum(player, deep) -> list:  # maximum aliases max
    if deep <= 1:return
    points = findMax(player, var.MAX_SCORE)  # points: a list of instances of playersScore
    if len(points) and points[0].score >= s.four: return [points[0]]
    elif len(points) == 0: return 
    else:
        for i,p in enumerate(points):
            board.put(p, player)
            if not p.score <= s.five: lastMaxPoint = p  # lastMaxPoint is an instance of playersScore
            m = minimum(P.reverse(player), deep - 1)        # m is a deque
            board.remove(p)
            if m:
                if len(m): return m.appendleft(p)
                else: return deque().append(p)
        return
            
def minimum(player, deep)-> list:
    w = board.win()
    if w == player: return False
    elif w == P.reverse(player): return True
    else:
        if deep <= 1: return False
        points = findMin(player, var.MIN_SCORE)
        if len(points) == 0: return False
        elif len(points) and -points[0].score >= s.four: return False
    candidates = []
    for i,p in enumerate(points):
        board.put(p, player)
        lastMaxPoint = p
        m = max(P.reverse(player), deep - 1)
        board.remove(p)
        if m:
            if len(m): 
                candidates.append(m.appendleft(p))
        else: return False
    return candidates[floor(len(candidates)*random())]

def findMax(player, score) -> list:
    result = []
    fives = []
    for i in range(board.size):
        for j in range(len(board.board[i])):
            if board.board[i][j] == P.empty:
                place = playersScore(i, j)
                if board.humScore[place.pos[0]][place.pos[1]] >= s.five:
                    place.score = s.five
                    if player == P.com: place.score *= -1
                    fives.append(place.pos)
                elif board.comScore[place.pos[0]][place.pos[1]] >= s.five:
                    place.score =s.five
                    if player == P.com: place.score *= -1
                    fives.append(place)
                elif (not lastMaxPoint) or i == lastMaxPoint.pos[0] or j == lastMaxPoint.pos[1] \
                or abs(i - lastMaxPoint.pos[0]) == abs(j - lastMaxPoint.pos[1]):
                    if player == P.com:
                        place.score = board.comScore[place.pos[0]][place.pos[1]] 
                    else: 
                         place.score = board.humScore[place.pos[0]][place.pos[1]]
                    if s > score: result.append(place)
    if len(fives): return fives
    return result.sort(place)

def findMin(player, score) -> list:
    result = []
    fives, fours, blocked_fours = [], deque(), deque()
    for i in range(board.size):
        for j in range(board.size):
            if board.board[i][j] == P.empty:
                place = playersScore(i, j)
                if player == P.com:
                    s1 = board.comScore[place.pos[0]][place.pos[1]]
                    s2 = board.humScore[place.pos[0]][place.pos[1]]
                else:
                    s1 = board.humScore[place.pos[0]][place.pos[1]]
                    s2 = board.comScore[place.pos[0]][place.pos[1]]
                    if s1 >= s.five:
                        place.score = -s1
                        return [place]
                    if s2 >= s.five:
                        place.score = s2
                        fives.append(place)
                    elif s1 >= s.four:
                        place.score = -s1
                        fours.appendleft(place)
                    elif s2 >= s.four:
                        place.score = s2
                        fours.append(place)
                    elif s1 >= s.blocked_four:
                        place.score = -s1
                        blocked_fours.appendleft(place)
                    elif s2 >= s.blocked_four:
                        place.score = s2
                        blocked_fours.append(place)
                    elif s1 >= score or s2 >= score:
                        place.score = s1     # shouldn't it be -s1 ?
                    result.append(place)
    if len(fives): return fives
    elif len(fours): return fours + blocked_fours
    else:
        result = blocked_fours + result
        return result.sort()

def cache(result, vcf: bool) -> None:   # cache the result and return it
    if not config.cache: return
    if vcf: var.Cache['VCF'][z.code] = result
    else: var.Cache['VCT'][z.code] = result
    return result

def getCache(vcf: bool):
    if not config.cache: return
    if vcf: result = var.Cache['VCF'][z.code]
    else: result = var.Cache['VCT'][z.code]
    return result

def deeping(player, deep):      # totalDeep eliminated
    for i in range(1,deep + 1):
        lastMaxPoint =playersScore()
        result = max(player, i, deep)
        if result: return result

def vcx(player, onlyFour: bool, deep=config.vcxDeep):
    if deep <= 0: return
    else:
        result = deeping(player, deep)
        if onlyFour:
            var.MAX_SCORE = s.blocked_four
            var.MIN_SCORE = s.five
            result.score = s.four
        else:
            var.MAX_SCORE = s.three
            var.MIN_SCORE = s.blocked_four
            result.score = s.three*2
    return result

def vcf(player, deep):
    if getCache(True): return getCache(True)
    else: return cache(vcx(player, True, deep), True)

def vct(player, deep):
    if getCache(False): return getCache(False)
    else: return cache(vcx(player, False, deep), False)