from score import scores as s
from score import players as P
import config
from board import board, playersScore
from time import perf_counter
from math import ceil
from random import choice

# ToDo:
#   1. rearrange deeping's result --done
#   2. comprehend r function --done
class var:
    MAX = s.five*10
    MIN = -MAX
    count, PVcut, ABcut = 0, 0, 0
    Cache = {}
    start_counter: float = 0
    index = 0

def negamax(candidates, player:int, deep:int, alpha, beta) -> int:
    if config.debug or config.gen: print([i.pos for i in candidates])
    var.count, var.PVcut, var.ABcut = 0, 0, 0 #參數歸零
    board.currentSteps = []
    for i in range(len(candidates)):   #遍歷所有可能的應手
        c = candidates[i] # replace p of c, is an instance of playersScore
        board.put(player, c)
        v: dict = r(deep-1, -beta, -alpha, P.reverse(player), 1, [c], 0)
        v['score'] *= -1
        alpha = max(alpha, v['score'])
        if config.debug: print(f'alpha: {alpha}')
        board.remove(c)
        c.v = v         # 該點經由後續遞迴的得出的分數
        timeSpent = perf_counter() - var.start_counter
        if  timeSpent > config.timeLimit: 
            print('time out!'); break
        if config.log:
            print(f'迭代完成, deep = {deep}, 耗時 {perf_counter() - var.start_counter} s.')
            # vct; vcf
    return alpha #回傳最佳解
# 遞迴搜索(step: 總步數, steps: 所有棋步, spread: 延伸搜索次數)
def r(deep, alpha, beta, player, step: int,steps: list, spread) -> dict:
    #1. 檢查此棋型是否已被搜索過 
    if config.cache:
        for i in var.Cache:
            if i == board.z.code:
                if config.debug: print('cache') 
                c = var.Cache[i] #z.code: 每個棋型的代號 
                if c['deep'] >= deep:  #暫存結果的搜索深度大於當前深度則可用
                    return {'score': c['score'], 'steps': steps, 'step': step + c['step'],\
                         'c': c, 'ABcut': 0}
                elif abs(c['score']) >= s.four: #搜索深度小於當前深度，則當一方有活四以上結果時可用
                    return {'score': c['score'], 'step': c['step'], 'steps': c['steps'], 'ABcut': 0}
    #2. 檢查此棋型自己是否已經可贏
    Eval = board.evaluate(player)  # 自己與對手的分數差距
    leaf = {'score':Eval, 'step':step, 'steps': steps, 'ABcut': 0} #搜索終點
    var.count += 1
    if deep < 0 or abs(Eval) >= s.five: return leaf
    # 分數差大於s.five: 某方已經可以單獨成五(勝利)，回傳leaf
    #3. 列出所有可能的下一步
    best: dict = {'score': var.MIN, 'step': step, 'steps': steps, 'ABcut': 0}  #?? why score is var.MIN?
    points = board.generator(player,step > 1 if board.count > 10 else step > 3, step > 1) #雙方各下一子，開始starSpread
    if not len(points): return leaf #沒有可下的點
    #if config.debug: print(f'A~B: {alpha} ~ {beta}')
    for i in range(len(points)):
        if perf_counter() - var.start_counter > config.timeLimit: break
        p = points[i]
        board.put(player, p)
        N_deep = deep -1
        N_spread = spread #??what is spread?
        if spread < config.spreadLimit: #沖四延伸
            if (player == P.com and p.scoreCom >= s.five)\
                or (player == P.hum and p.scoreHum >= s.five): #! exchange scoreCom & scoreHum
                N_deep += 2; spread += 1  #加兩層深度
        N_steps = steps.copy()
        N_steps.append(p)
        v :dict = r(N_deep, -beta, -alpha, P.reverse(player), step+1, N_steps, N_spread)
        v['score'] *= -1
        board.remove(p)
        if v['score'] > best['score']: best = v #搜索的score比當前最佳解還好
        alpha = max(best['score'], alpha)  #alpha剪枝
        if v['score'] > beta:
            if config.debug: print('beta pruning!')
            var.ABcut += 1
            v['score'] = var.MAX - 1 #被剪枝，用一個大值來記錄
            v['ABcut'] = 1
            return v
    # concatenate the cache function here
    if config.cache and best['ABcut'] != 1:
        var.Cache.setdefault(board.z.code, {
            'deep': deep, 'score': best['score'],\
            'step': best['step'], 'steps': best['steps'],\
            'board': str(board)})
    return best
    
def deeping(candidates: list, player, deep = config.searchDeep):
    var.start_counter = perf_counter()
    if config.clear_cache: var.Cache = {}  #清空暫存
    for i in range(2, deep + 1, 2):  #從兩層開始逐漸加深到指定的deep
        if negamax(candidates, player, i, var.MIN , var.MAX) >= s.five: 
            if config.debug or config.gen: print('win')
            break 
    #可贏，跳出
    chosen, choices = [], []
    if config.log: 
        for i in candidates: print(i.v)
    for k in range(ceil(len(candidates)/5)): #randomly pick good candidates
        result = candidates[0]
        try:
            for j, i in enumerate(candidates[1:]):
                if i.v['ABcut'] == 1: continue #raise Exception('pruning bugs?')
                if j in chosen: continue
                if i.v['score'] > result.v['score']: result = i; var.index = j
                elif i.v['score'] == result.v['score']:
                    if i.v['score'] >= 0 and i.v['step'] < result.v['step']:  #若會贏，選擇步數最短的走法
                        result = i; var.index = j
                    elif i.v['score'] < 0 and i.v['step'] > result.v['step']: #若會輸，選擇步數最長的走法拖延
                        result = i; var.index = j 
            result.score = result.v['score']
        except: KeyError
        choices.append(result)
        if config.log or config.gen: 
            print(var.index)
            print(result.v)
        chosen.append(var.index)
    return  choice(choices) #playersScore()

def deepAll(deep = config.searchDeep):
    return deeping(board.generator(P.com, False, config.starSpread), P.com, deep)
    #0表示不開啟onlyThree模式