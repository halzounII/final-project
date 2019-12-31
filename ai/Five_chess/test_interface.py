import pygame as pg
from pygame.locals import *

BACKGROUND = r'C:\TMP\w15\final-project\ai\Five_chess\ramin.jpg'                       # 棋盤圖 from github
BOARD_SIZE = (820, 820)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


class Board(object):                           # 棋盤
    def __init__(self):
        self.groups = []
        self.next = BLACK
        self.outline = pg.Rect(45, 45, 720, 720)
        self.draw()
        
    def draw(self):
        pg.draw.rect(background, BLACK, self.outline, 3)
        # Outline is inflated here for future use as a collidebox for the mouse
        self.outline.inflate_ip(20, 20)
        for i in range(18):
            for j in range(18):
                rect = pg.Rect(45 + (40 * i), 45 + (40 * j), 40, 40)
                pg.draw.rect(background, BLACK, rect, 1)
        for i in range(3):
            for j in range(3):
                coords = (165 + (240 * i), 165 + (240 * j))
                pg.draw.circle(background, BLACK, coords, 5, 0)
        screen.blit(background, (0, 0))                                 # 重繪視窗
        pg.display.update()                                             # 更新視窗

def Setting():
    font = pg.font.SysFont("simhei", 40) 
    text_G = font.render("Game continues?", True, (0,255,0), (255,255,255)) 
    text_Y = font.render("Yes", True, (0,0,255), (255,255,255)) 
    text_N = font.render("No", True, (255,0,0), (255,255,255)) 
    screen.blit(text_G, (285,240))
    screen.blit(text_Y, (380,280))
    screen.blit(text_N, (385,320))
    pg.display.update()
    Yes_outline = pg.Rect(380,280,50,20)
    No_outline  = pg.Rect(385,320,40,20)
    s_hit = pg.mixer.Sound('Wate.wav')  #括弧為音檔名稱 
    s_hit.set_volume(0.7)  #設定音量大小，參值0~1 
    run = True
    while run:
        for event in pg.event.get():   
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1 and Yes_outline.collidepoint(event.pos):
                    s_hit.play()
                    run =False
                elif event.button == 1 and No_outline.collidepoint(event.pos):
                    s_hit.play()
                    pg.time.wait(300)
                    exit()    
    screen.blit(background,(0,0))
    pg.display.update()           
    pg.time.wait(300)
    text_L1 = font.render("Easy", True, (0,0,255), (255,255,255)) 
    text_L2 = font.render("Normal", True, (0,0,255), (255,255,255)) 
    text_L3 = font.render("Hard", True, (0,0,255), (255,255,255)) 
    screen.blit(text_L1, (373,240))
    screen.blit(text_L2, (357,280))
    screen.blit(text_L3, (371,320))
    pg.display.update()
    L1_outline = pg.Rect(380,240,50,20)
    L2_outline = pg.Rect(380,280,50,20)
    L3_outline = pg.Rect(380,320,50,20)
    run = True
    while run:
        for event in pg.event.get():   
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1 and L1_outline.collidepoint(event.pos):
                    s_hit.play()
                    run =False
                    level=1
                elif event.button == 1 and L2_outline.collidepoint(event.pos):
                    s_hit.play()
                    run =False
                    level=2
                elif event.button == 1 and L3_outline.collidepoint(event.pos):
                    s_hit.play()
                    run =False
                    level=3
    screen.blit(background,(0,0))
    pg.display.update()
    pg.time.wait(300)
    return level

if __name__ == '__main__':
    pg.init()
    pg.display.set_caption('Goban')
    screen = pg.display.set_mode(BOARD_SIZE, 0, 32)
    background = pg.image.load(BACKGROUND)
    board = Board()

    level=Setting()
    print("Level",level)