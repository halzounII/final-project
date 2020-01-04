# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 17:36:16 2019

@author: sab93
"""

import pygame as pg
from pygame.locals import *
from ai_modified import auto, bk


BACKGROUND = 'D:/Users/sab93/Desktop/python/final-project/ai/Five_chess/ramin.jpg'                       # 棋盤圖 from github
BTN1 = 'D:/Users/sab93/Desktop/python/final-project/ai/Five_chess/regret0.png'
BTN2 = 'D:/Users/sab93/Desktop/python/final-project/ai/Five_chess/regret1.png'
BOARD_SIZE = (820, 820)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

class Stone(object):                           # 棋子
    def __init__(self, rboard, point, color):
        """Create and initialize a stone.
        Arguments:
        board -- the board which the stone resides on
        point -- location of the stone as a tuple, e.g. (3, 3)
                 represents the upper left hoshi
        color -- color of the stone
        """
        self.rboard = rboard                     
        self.point = point                     # 相對位置
        self.color = color
        self.coords = (5 + self.point[0] * 40, 5 + self.point[1] * 40)    # 棋盤實際位置
        
    def draw(self):
        """Draw the stone as a circle."""
        pg.draw.circle(screen, self.color, self.coords, 20, 0)            #(Surface, color, pos , raduis, width)
        pg.display.update()
        

    
    def remove(self):                                                     # 移除(悔棋)
        """Remove the stone from board."""
        blit_coords = (self.coords[0] - 20, self.coords[1] - 20)
        area_rect = pg.Rect(blit_coords, (40, 40))
        screen.blit(background, blit_coords, area_rect)
        pg.display.update()
        #self.group.stones.remove(self)
        del self


        
class RealBoard(object):                           # 棋盤
    def __init__(self):
        """Create and initialize an empty board."""
        self.groups = {(0, 0, 0):[], (255, 255, 255):[]}
        self.next = BLACK
        self.outline = pg.Rect(45, 45, 560, 560)   # (起始x y x長 y長 )
        #self.regret = pg.Rect(625, 45, 150 ,75)
        self.draw()
        self.bk = False
        
    def draw(self):
        """Draw the board to the background and blit it to the screen.
        The board is drawn by first drawing the outline, then the 19x19
        grid and finally by adding hoshi to the board. All these
        operations are done with pygame's draw functions.
        This method should only be called once, when initializing the
        board.
        """
        pg.draw.rect(background, BLACK, self.outline, 3)
        #pg.draw.rect(background, (255, 0, 0), self.regret, 0)
        # Outline is inflated here for future use as a collidebox for the mouse
        self.outline.inflate_ip(20, 20)            #原地放大縮小 用處??
        for i in range(14):
            for j in range(14):
                rect = pg.Rect(45 + (40 * i), 45 + (40 * j), 40, 40)
                pg.draw.rect(background, BLACK, rect, 1)
        for i in range(2):
            for j in range(2):
                coords = (165 + (320 * i), 165 + (320 * j))
                pg.draw.circle(background, BLACK, coords, 5, 0)
        screen.blit(background, (0, 0))                                 # 重繪視窗(棋盤背景)
        screen.blit(btn[0], (650, 45))                                  # 畫按鈕
        pg.display.update()                                             # 更新視窗

    def search(self, point=None, points=[]):
        """Search the board for a stone.
        The board is searched in a linear fashion, looking for either a
        stone in a single point (which the method will immediately
        return if found) or all stones within a group of points.
        Arguments:
        point -- a single point (tuple) to look for
        points -- a list of points to be searched
        """

        if point in self.groups[WHITE] or point in self.groups[BLACK] :
            return True
        else:
            self.groups[self.next].append(point)
            print(f"黑棋位置{self.groups[0,0,0]}\n白棋位置{self.groups[(255,255,255)]}")
            return False

    def check_win(self, x, y, color):
        
        first = [[x-4, y-4], [x-4, y+4], [x-4, y], [x, y-4]]
        count = 0
        for j in range(4):
            x = first[j][0]
            y = first[j][1]
            if j == 0:
                for i in range(9):
                    if (x+i, y+i) in self.groups[color]:
                        count += 1
                        #print(count)
                        if count == 5:
                            return True
                    else:
                        count = 0
            if j == 1:
                for i in range(9):
                    if (x+i, y-i) in self.groups[color]:
                        count += 1
                       # print(count)
                        if count == 5:
                            return True
                    else:
                        count = 0
            if j == 2:
                for i in range(9):
                    if (x+i, y) in self.groups[color]:
                        count += 1
                        #print(count)
                        if count == 5:
                            return True
                    else:
                        count = 0
            if j == 3:
                for i in range(9):
                    if (x, y+i) in self.groups[color]:
                        count += 1
                        #print(count)
                        if count == 5:
                            return True
                    else:
                        count = 0
            
        return False

    def win(self, color):
        font = pg.font.Font("D:/Users/sab93/Desktop/python/final-project/ai/Five_chess/msjh.ttc", 50)
        if color == WHITE:
            text = font.render("你贏了 蒸蚌", True, (0,0,255), (255,255,255))
            screen.blit(text, (200,250))
        else:
            text = font.render("哈哈哈哈哈", True, (0,0,255), (255,255,255))
            screen.blit(text, (200,250))
        pg.display.update()

    
    @staticmethod    
    def Preview():
        pos = pg.mouse.get_pos()
        x = int(round(((pos[0] - 5) / 40.0), 0))*40-5
        y = int(round(((pos[1] - 5) / 40.0), 0))*40-5
        stone = rboard.search(point=(x, y))
        print(stone)
        if not stone:
            preview = pg.Rect([x, y, 20, 20])           
            pg.draw.rect(screen, RED, preview, 1)
            pg.display.update()
            pg.time.wait(30)
            blit_coords = (x , y )
            area_rect = pg.Rect(blit_coords, (20, 20))
            screen.blit(background, blit_coords, area_rect)
            pg.display.update()

    def turn(self):
        """Keep track of the turn by flipping between BLACK and WHITE."""
        if self.next == BLACK:
            self.next = WHITE
            return BLACK
        else:
            self.next = BLACK
            return WHITE

    def auto_draw(self, x, y):

        print(x, y)
        added_stone = Stone(rboard, (x, y), rboard.turn())
        added_stone.draw()
        
def GUI():
    #pg.init()                                   # 初始化
    #window = pg.display.set_mode((900,900))     # 建視窗
    run = True
    #rboard.search(point=(8, 8))
    #added_stone = Stone(rboard, (8, 8), rboard.turn())
    #added_stone.draw()
    rboard.next = WHITE

    
    while run:
        for event in pg.event.get():   
            
            #RealBoard.Preview()
            #print(pos,x,y)
            if event.type == KEYDOWN:           # 觸發關閉視窗
                if event.key == K_ESCAPE:
                    run = False
            elif event.type == QUIT:
                run = False

            elif event.type == pg.MOUSEBUTTONDOWN:  # 下棋
                if event.button == 1 and rboard.outline.collidepoint(event.pos):            
                    x = int(round(((event.pos[0] - 5) / 40.0), 0))
                    y = int(round(((event.pos[1] - 5) / 40.0), 0))
                    stone = rboard.search(point=(x, y))
                    if not stone :
                        added_stone = Stone(rboard, (x, y), rboard.turn())
                        added_stone.draw()                       # 玩家下(先手 白 )
                        if rboard.check_win(x,y, WHITE):
                            print('win')
                            rboard.win(WHITE)
                        print("checked")
                        a, b = auto(y-1,x-1)                     
                        #print(a,b)
                        if not rboard.search(point=(b+1,a+1)):   # 有時會沒下到(可能重複下) 擋活三死四時發生
                            rboard.auto_draw(b+1,a+1)                    # 電腦下
                            if rboard.check_win(b+1,a+1, BLACK):
                                print("lose")
                                rboard.win(BLACK)
                            rboard.next = WHITE
                        
                
                if event.button == 1 and btn_rect.collidepoint(event.pos):
                   
                    if rboard.groups[(255, 255, 255)] and rboard.groups[(0, 0, 0)]: 
                        print("悔棋")
                        # 按下動畫
                        screen.blit(btn[1], (650, 45))
                        pg.display.update()
                        pg.time.wait(150)
                        screen.blit(btn[0], (650, 45))
                        pg.display.update()
                        # 動作
                        bk()
                        removed_w = Stone(rboard, (rboard.groups[(255, 255, 255)].pop()), WHITE )
                        removed_w.remove()
                        removed_b = Stone(rboard, (rboard.groups[(0, 0, 0)].pop()), BLACK )
                        removed_b.remove()                       
    exit()
    
    
    
    
if __name__ == '__main__':
    pg.init()
    pg.display.set_caption('五子棋')                     # 視窗標題
    screen = pg.display.set_mode(BOARD_SIZE, 0, 32)      # 視窗
    background = pg.image.load(BACKGROUND).convert()     
    btn = [pg.image.load(BTN1).convert_alpha(), pg.image.load(BTN2).convert_alpha()] # 按鈕圖
    btn_rect = btn[0].get_rect(topleft=(650, 45))  # 獲取矩形區域
    rboard = RealBoard()
    GUI()
    '''
    ai = AI()
    ai.begin()
    print(board)
    
    while True:
        x,y = int(input('x:')), int(input('y:'))
        board.put(P.hum, playersScore(x, y))
        ai.begin()
        print(board)
        table, table2 = '', ''
        for i in range(15):
            table += ''.join(str(board.humScore[i])) + '\n'
            table2 += ''.join(str(board.comScore[i])) + '\n'
        #print(table)
        #print(table2)
        #print(board.allSteps)   
    '''