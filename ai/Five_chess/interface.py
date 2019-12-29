# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 17:36:16 2019

@author: sab93
"""

import pygame as pg
from pygame.locals import *

BACKGROUND = r'D:\final project\final-project\ai\Five_chess\ramin.jpg'                       # 棋盤圖 from github
BOARD_SIZE = (820, 820)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

class Stone(object):                           # 棋子
    def __init__(self, board, point, color):
        """Create and initialize a stone.
        Arguments:
        board -- the board which the stone resides on
        point -- location of the stone as a tuple, e.g. (3, 3)
                 represents the upper left hoshi
        color -- color of the stone
        """
        self.board = board                     
        self.point = point                     # 相對位置
        self.color = color
        self.coords = (5 + self.point[0] * 40, 5 + self.point[1] * 40)    # 棋盤實際位置
        
    def draw(self):
        """Draw the stone as a circle."""
        pg.draw.circle(screen, self.color, self.coords, 20, 0)            #(Surface, color, pos , raduis, width)
        pg.display.update()
        

    
    def remove(self):
        """Remove the stone from board."""
        blit_coords = (self.coords[0] - 20, self.coords[1] - 20)
        area_rect = pg.Rect(blit_coords, (40, 40))
        screen.blit(background, blit_coords, area_rect)
        pg.display.update()
        #self.group.stones.remove(self)
        del self


        
class Board(object):                           # 棋盤
    def __init__(self):
        """Create and initialize an empty board."""
        self.groups = []
        self.next = BLACK
        self.outline = pg.Rect(45, 45, 720, 720)
        self.draw()
        
    def draw(self):
        """Draw the board to the background and blit it to the screen.
        The board is drawn by first drawing the outline, then the 19x19
        grid and finally by adding hoshi to the board. All these
        operations are done with pygame's draw functions.
        This method should only be called once, when initializing the
        board.
        """
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

    def search(self, point=None, points=[]):
        """Search the board for a stone.
        The board is searched in a linear fashion, looking for either a
        stone in a single point (which the method will immediately
        return if found) or all stones within a group of points.
        Arguments:
        point -- a single point (tuple) to look for
        points -- a list of points to be searched
        """
        stones = []
        for group in self.groups:
            for stone in group.stones:
                if stone.point == point and not points:
                    return stone
                if stone.point in points:
                    stones.append(stone)
        
        return stones
    
    @staticmethod    
    def Preview():
        pos = pg.mouse.get_pos()
        x = int(round(((pos[0] - 5) / 40.0), 0))*40-5
        y = int(round(((pos[1] - 5) / 40.0), 0))*40-5
        stone = board.search(point=(x, y))
        #print(stone)
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
        
def GUI():
    #pg.init()                                   # 初始化
    #window = pg.display.set_mode((900,900))     # 建視窗
    run = True
    while run:
        for event in pg.event.get():   

            Board.Preview()
            #print(pos,x,y)
            if event.type == KEYDOWN:           # 觸發關閉視窗
                if event.key == K_ESCAPE:
                    run = False
            elif event.type == QUIT:
                run = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1 and board.outline.collidepoint(event.pos):            
                    x = int(round(((event.pos[0] - 5) / 40.0), 0))
                    y = int(round(((event.pos[1] - 5) / 40.0), 0))
                    stone = board.search(point=(x, y))
                    if stone:
                        stone.remove()
                    else:
                        #print(x, y)
                        added_stone = Stone(board, (x, y), board.turn())
                        added_stone.draw()
                    #board.update_liberties(added_stone)
    exit()
    
    
    
    
if __name__ == '__main__':
    pg.init()
    pg.display.set_caption('Goban')
    screen = pg.display.set_mode(BOARD_SIZE, 0, 32)
    background = pg.image.load(BACKGROUND)
    board = Board()
    GUI()
    