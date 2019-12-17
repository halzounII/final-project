from score import scores as s
from score import players as P
import config
from board import board
from time import perf_counter

class var:
    MAX = s.five*10
    MIN = -MAX
    count, PVcut, ABcut = 0, 0, 0
    Cache = {}
    start_counter: float

def negamax(candidates:list, player:int, deep:int, alpha, beta):
    for i in range(len(candidates)):
        c = candidates[i] # replace p of c
        board.put(c, player)
        v = r(deep-1, -beta, -alpha, P.reverse(player), 1, c, 0)
        v.score *= -1
        alpha = max(alpha, v.score)
        board.remove(c)
        c.v = v
        if perf_counter() - var.start_counter > config.timeLimit*1000: break
    return alpha

def r(deep, alpha, beta, player, step ,steps, spread) -> dict:
    if config.cache:
        c = var.Cache[board.z.code]
        if c:
            if c.deep >= deep:
                return {'score': c['score'], 'steps': steps, 'step': step + c['step']}
            #elif abs(c['score']) >= s.four: optional
    Eval = board.evaluate(player)  # replace _e of Eval
    leaf = {'score':Eval, 'step':step, 'steps': steps}
    var.count += 1
    if deep <= 0 or Eval >= s.five or Eval <= -s.five: return leaf
    
    best = {'score': var.MIN, 'step': step, 'steps': steps}
    points = board.generator(player,step > 1 if board.count > 10 else step > 3, step > 1)
    if not len(points): return leaf
    pass # debug
    for i in range(len(points)):
        p = points[i]
        board.put(p, player)
        N_deep = deep -1
        N_spread = spread
        if spread < config.spreadLimit:
            if (player == P.com and p.scoreHum >= s.five)\
                or (player == P.hum and p.scoreCom >= s.five):
                N_deep += 2; spread += 1
        N_steps = steps
        N_steps.append(p)
        v = r(N_deep, alpha, beta, P.reverse(player), step+1, N_steps, N_spread)
        v.score *= -1
        board.remove(p)

        if v.score > best['score']: best = v
        alpha = max(best.score, alpha)
        if v.score > beta:
            var.ABcut += 1
            v.score = var.MAX - 1
            v.ABcut = 1
            return v
    # concatenate the cache function here
    if config.cache:
        var.Cache.setdefault(board.z.code, {
            'deep': deep, 'score': v.score,\
            'steps': steps, 'step': step,\
            'board': str(board)})
    return best

def deeping(candidates, player, deep):
    start_counter = perf_counter()
    var.Cache = {}
    for i in range(2, deep + 1, 2):
        if negamax(candidates, player, i, var.MIN , var.MAX) >= s.five: break
    pass # rearrange candidates and find the best one
    timeSpent = perf_counter() - start_counter
    print(timeSpent)
    return candidates[0]

def deepAll(player = P.com, deep = config.searchDeep):
    Candidates = board.generator(player, 0 , config.starSpread)
    return deeping(Candidates, player, deep)