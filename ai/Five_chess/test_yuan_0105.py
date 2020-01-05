# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 17:36:16 2019

@author: sab93
"""

from pygame import draw, display, Rect, mouse, event, time, init, image
from pygame.locals import K_ESCAPE, KEYDOWN, MOUSEBUTTONDOWN, QUIT
from ai import ai
from board import board, playersScore
from score import players as P
from os import getcwd
import pygame as pg
import config
BACKGROUND = getcwd().replace('\\', '/') + '/ramin.jpg'# 棋盤圖 from github
BTN1 = getcwd().replace('\\', '/') + '/regret0.png'
BTN2 = getcwd().replace('\\', '/') + '/regret1.png'
BTN_location = (650, 60)
BOARD_SIZE = (820, 700)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
Stones = []
class Stone(object):                           # 棋子
    def __init__(self, rboard, point, color = None):
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
        self.coords = (5 + self.point[0] * 40, 25 + self.point[1] * 40)    # 棋盤實際位置
        
    def draw(self):
        """Draw the stone as a circle."""
        draw.circle(background, BLACK if rboard.next == WHITE else WHITE, self.coords, 20, 0)            #(Surface, color, pos , raduis, width)
        screen.blit(background, (0, 0))
        display.update()
        

    
    def remove(self):                                                     # 移除(悔棋)
        """Remove the stone from board."""
        blit_coords = (self.coords[0] - 20, self.coords[1] - 20)
        area_rect = Rect(blit_coords, (40, 40))
        background.blit(background_org, blit_coords, area_rect)
        screen.blit(background, (0, 0))
        # screen.blit(background, blit_coords, area_rect)
        display.update()
        #self.group.stones.remove(self)
        del self


class RealBoard(object):                           # 棋盤
    def __init__(self):
        """Create and initialize an empty board."""
        self.groups = {(0, 0, 0):[], (255, 255, 255):[]}
        self.next = WHITE
        self.outline = Rect(45, 65, 560, 560)   # (起始x y x長 y長 )
        self.regret = Rect(625, 65, 150 ,75)
        self.draw()
        background_org.blit(background, (0, 0))
        self.bk = False
        
    def draw(self):
        """Draw the board to the background and blit it to the screen.
        The board is drawn by first drawing the outline, then the 19x19
        grid and finally by adding hoshi to the board. All these
        operations are done with pygame's draw functions.
        This method should only be called once, when initializing the
        board.
        """
        draw.rect(background, BLACK, self.outline, 3)
        #draw.rect(background, BLACK, self.regret, 3)
        # Outline is inflated here for future use as a collidebox for the mouse
        self.outline.inflate_ip(20, 20)            #原地放大縮小 用處??
        for i in range(14):
            for j in range(14):
                rect = Rect(45 + (40 * i), 65 + (40 * j), 40, 40)
                draw.rect(background, BLACK, rect, 1)
        for i in range(2):
            for j in range(2):
                coords = (165 + (320 * i), 185 + (320 * j))
                draw.circle(background, BLACK, coords, 5, 0)
        screen.blit(background, (0, 0))                                 # 重繪視窗
        background.blit(btn[0], BTN_location)                                  # 畫按鈕
        display.update()                                             # 更新視窗

    def search(self, point=None, points=[], redRect = False):
        """Search the board for a stone.
        The board is searched in a linear fashion, looking for either a
        stone in a single point (which the method will immediately
        return if found) or all stones within a group of points.
        Arguments:
        point -- a single point (tuple) to look for
        points -- a list of points to be searched
        """

        for i in Stones:
            if point == i.point: return True
        if not redRect:
            self.groups[self.next].append(point)
            print(f"黑棋位置{self.groups[0,0,0]}\n白棋位置{self.groups[(255,255,255)]}")
            return False
 
    @staticmethod    
    def Preview():
        pos = mouse.get_pos()
        x = int(round(((pos[0] - 5) / 40.0), 0))*40-5
        y = int(round(((pos[1] - 25) / 40.0), 0))*40+15
        stone = rboard.search(point=(x, y), redRect = True)
        #print(stone)
        if not stone and (25<=x<=625) and (45<=y<=645):
            preview = Rect([x, y, 20, 20])           
            draw.rect(screen, RED, preview, 1)
            display.update()
            time.wait(50)
            blit_coords = (x , y )
            area_rect = Rect(blit_coords, (20, 20))
            screen.blit(background, blit_coords, area_rect)
            display.update()

    def turn(self):
        """Keep track of the turn by flipping between BLACK and WHITE."""
        if self.next == BLACK:
            self.next = WHITE
            return BLACK
        else:
            self.next = BLACK
            return WHITE

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
        if color == BLACK:
            text = font.render("你贏了", True, (0,0,255), (255,255,255))
            screen.blit(text, (200,250))
        else:
            text = font.render("你輸了", True, (0,0,255), (255,255,255))
            screen.blit(text, (200,250))
        pg.display.update()
        paused()

def paused():
    while True:
        for _event in pg.event.get():
            print(_event)
            if _event.type == pg.QUIT:
                pg.quit()

    #def auto_draw(self, x, y):
    #    print(x, y)
    #    added_stone = Stone(rboard, (x, y), rboard.turn())
    #    added_stone.draw()
#def adjust_window():

        
def GUI():
    s_hit = pg.mixer.Sound('Wate.wav')  #括弧為音檔名稱 
    s_hit.set_volume(0.7)  #設定音量大小，參值0~1 
    #window = pg.display.set_mode((900,900))     # 建視窗
    run = True
    font = pg.font.Font("msjhbd.ttc", 28)
    #regret_str = font.render('悔棋', True, (255,0,0), (224,224,80))
    #background.blit(regret_str, (670,80))
    screen.blit(background,(0,0))
    background.blit(btn[0], BTN_location)                                  # 畫按鈕
    pg.display.update()
    #regret_outline  = pg.Rect(625, 65, 150 ,75)
    start_ticks=pg.time.get_ticks() #將目前的時間記錄下來, 單位是毫秒
    rboard.next = BLACK
    while run:

        T_count = 30 - (pg.time.get_ticks()-start_ticks)/1000  #倒數20秒 兩個時間差, 單位是毫秒
        if T_count < 0:
            count_time = font.render('時間到了!', True, (255,0,0), (000,255,255)) 
            screen.blit(count_time, (345,0))
            pg.display.update()
            s_kill = pg.mixer.Sound('kill.wav')  #括弧為音檔名稱 
            s_kill.set_volume(0.7)  #設定音量大小，參值0~1
            s_kill.play() 
            pg.time.wait(2000)
            count_time = font.render('你輸了!!!', True, (255,0,0), (000,255,255)) 
            screen.blit(count_time, (345,0))
            pg.display.update()
            pg.time.wait(1500)
            quit()
        else:
            count_time_str = f'{T_count:04.1f}'
            count_time = font.render(count_time_str, True, (0,0,255), (224,224,80)) 
            screen.blit(count_time, (377,0))
            pg.display.update()

        for _event in event.get():
            RealBoard.Preview()
            #print(pos,x,y)
            if _event.type == KEYDOWN:           # 觸發關閉視窗
                if _event.key == K_ESCAPE:
                    run = False
            elif _event.type == QUIT:
                run = False

            elif _event.type == MOUSEBUTTONDOWN:  # 下棋
                if _event.button == 1 and rboard.outline.collidepoint(_event.pos):            
                    x = int(round(((_event.pos[0] - 5) / 40.0), 0))
                    y = int(round(((_event.pos[1] - 25) / 40.0), 0))
                    stone = rboard.search(point=(x, y))

                    if not stone :
                        hum_stone = Stone(rboard, (x, y), rboard.turn())
                        Stones.append(hum_stone)
                        hum_stone.draw()                       # 玩家下(先手 黑 )
                        if rboard.check_win(x,y, BLACK):
                            rboard.win(BLACK)
                            
                        board.put(P.hum, playersScore(y-1,x-1))
                        s_hit.play()

                        a, b = tuple(ai.begin().pos)
                        start_ticks=pg.time.get_ticks() #AI下完棋後, 將目前的時間記錄下來, 單位是毫秒                   
                        if not rboard.search(point=(b+1,a+1)):   # 有時會沒下到(可能重複下) 擋活三死四時發生
                            com_stone = Stone(rboard, (b+1, a+1), rboard.turn())
                            Stones.append(com_stone)
                            com_stone.draw()
                            if rboard.check_win(b+1,a+1, WHITE):
                                rboard.win(WHITE)
                                
                    else: 
                        screen.blit(font.render("該位置已有棋子存在!", True, (255,0,0), (224, 224, 80)), (200,650))
                        display.update()
                        time.wait(500)
                        screen.blit(background, (0, 0))
                        display.update()

                elif _event.button == 1 and btn_rect.collidepoint(_event.pos):
                    if rboard.groups[(255, 255, 255)] and rboard.groups[(0, 0, 0)]: 
                        # 按下動畫
                        screen.blit(btn[1], BTN_location)
                        pg.display.update()
                        pg.time.wait(150)
                        screen.blit(btn[0], BTN_location)
                        pg.display.update()
                        # 動作
                        start_ticks=pg.time.get_ticks()
                        #removed_b = Stone(rboard, (board.allSteps[-1].pos[1]+1, board.allSteps[-1].pos[0]+1))
                        Stones.pop().remove()
                        #removed_w = Stone(rboard, (board.allSteps[-2].pos[1]+1, board.allSteps[-2].pos[0]+1))
                        Stones.pop().remove()
                        ai.backward()                  
                        s_hit.play()
                        time.wait(200)
                '''
                elif _event.button == 1 and rboard.regret.collidepoint(_event.pos):
                    if rboard.groups[(255, 255, 255)] and rboard.groups[(0, 0, 0)]: 
                        if config.log:print("悔棋")
                        start_ticks=pg.time.get_ticks()
                        #removed_b = Stone(rboard, (board.allSteps[-1].pos[1]+1, board.allSteps[-1].pos[0]+1))
                        Stones.pop().remove()
                        #removed_w = Stone(rboard, (board.allSteps[-2].pos[1]+1, board.allSteps[-2].pos[0]+1))
                        Stones.pop().remove()
                        ai.backward()                  
                        s_hit.play()
                        time.wait(200)
                    #board.update_liberties(added_stone)
                '''
                        
                
    exit()

def Setting():  #難度設定
    font = pg.font.Font(getcwd().replace('\\','/') + '/msjhbd.ttc', 28) 
    text_G = font.render("繼續玩五子棋?", True, (0,0,255), (224,224,80)) 
    text_Y = font.render("是", True, (0,0,255), (224,224,80)) 
    text_N = font.render("否", True, (255,0,0), (224,224,80)) 
    screen.blit(text_G, (315,240))
    screen.blit(text_Y, (390,300))
    screen.blit(text_N, (390,360))
    display.update()
    Yes_outline = Rect(390,300,40,30)
    No_outline  = Rect(390,360,40,30)
    s_hit = pg.mixer.Sound('Wate.wav')  #括弧為音檔名稱 
    s_hit.set_volume(0.7)  #設定音量大小，參值0~1 
    run = True
    while run:
        for event in pg.event.get():   
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and Yes_outline.collidepoint(event.pos):
                    s_hit.play()
                    run =False
                elif event.button == 1 and No_outline.collidepoint(event.pos):
                    s_hit.play()
                    pg.time.wait(300)
                    exit()    
    screen.blit(background,(0,0))
    display.update()           
    time.wait(300)
    text_L1 = font.render("初級", True, (0,0,255), (224,224,80)) 
    text_L2 = font.render("中級", True, (0,0,255), (224,224,80)) 
    text_L3 = font.render("高級", True, (0,0,255), (224,224,80)) 
    screen.blit(text_L1, (377,240))
    screen.blit(text_L2, (377,300))
    screen.blit(text_L3, (377,360))
    display.update()
    L1_outline = Rect(377,240,50,30)
    L2_outline = Rect(377,300,50,30)
    L3_outline = Rect(377,360,50,30)
    run = True
    while run:
        for event in pg.event.get():   
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and L1_outline.collidepoint(event.pos):
                    s_hit.play()
                    run =False
                    level=2
                elif event.button == 1 and L2_outline.collidepoint(event.pos):
                    s_hit.play()
                    run =False
                    level=5
                elif event.button == 1 and L3_outline.collidepoint(event.pos):
                    s_hit.play()
                    run =False
                    level=8
    screen.blit(background,(0,0))
    display.update()
    time.wait(300)
    return level   
    
    
    
if __name__ == '__main__':
    init()
    display.set_caption('五子棋')
    screen = display.set_mode(BOARD_SIZE, pg.RESIZABLE, 32)
    background = image.load(BACKGROUND).convert()
    background_org = image.load(BACKGROUND).convert()
    btn = [pg.image.load(BTN1).convert_alpha(), pg.image.load(BTN2).convert_alpha()] # 按鈕圖
    btn_rect = btn[0].get_rect(topleft=BTN_location)  # 獲取矩形區域
    rboard = RealBoard()
    searchDeep=Setting()     # 執行難度設定, 並回傳難度值 (1~3)
    print("Level",searchDeep)
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