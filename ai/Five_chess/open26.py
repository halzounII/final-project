from board import matrix
from random import choice

board1, board2 = matrix(), matrix()
board1[7][7], board2[6][7] = 1, 2
board2[7][7], board2[6][8] = 1, 2
class open26:
    def __init__(self):
        self.shuyue = board1.copy()
        self.shuyue[5][5] = 1
        self.shuyue_name = '疏月'

        self.xiyue = board1.copy()
        self.xiyue[5][6] = 1
        self.xiyue_name = '溪月'

        self.hanyue = board1.copy()
        self.hanyue[5][7] = 1
        self.hanyue_name = '寒月'

        self.canyue = board1.copy()
        self.canyue[6][5] = 1
        self.canyue_name = '残月'

        self.huayue = board1.copy()
        self.huayue[6][6] = 1
        self.huayue_name = '花月'

        self.jinyue = board1.copy()
        self.jinyue[7][5] = 1
        self.jinyue_name = '金月'

        self.yuyue = board1.copy()
        self.yuyue[7][6] = 1
        self.yuyue_name = '雨月'

        self.xinyue = board1.copy()
        self.xinyue[8][5] = 1
        self.xinyue_name = '新月'

        self.qiuyue = board1.copy()
        self.qiuyue[8][6] = 1
        self.qiuyue_name = '丘月'

        self.songyue = board1.copy()
        self.songyue[8][7] = 1
        self.songyue_name = '松月'

        self.youyue = board1.copy()
        self.youyue[9][5] = 1
        self.youyue_name = '游月'

        self.shanyue = board1.copy()
        self.shanyue[9][6] = 1
        self.shanyue_name = '山月'

        self.ruiyue = board1.copy()   
        self.ruiyue[9][7] = 1
        self.ruiyue_name = '瑞月'
        
        self.liuyue = board2.copy()
        self.liuyue[5][5] = 1
        self.liuyue_name = '流月'

        self.shuiyue = board2.copy()
        self.shuiyue[5][6] = 1
        self.shuiyue_name = '水月'

        self.hengyue = board2.copy()
        self.hengyue[5][7] = 1
        self.hengyue_name = '恒月'

        self.xiayue = board2.copy()
        self.xiayue[5][8] = 1
        self.xiayue_name = '峡月'

        self.changyue = board2.copy()
        self.changyue[5][9] = 1
        self.changyue_name = '长月'

        self.lanyue = board2.copy()
        self.lanyue[6][5] = 1
        self.lanyue_name = '岚月'

        self.puyue = board2.copy()
        self.puyue[6][6] = 1
        self.puyue_name = '浦月'

        self.yunyue = board2.copy()
        self.yunyue[6][7] = 1
        self.yunyue_name = '云月'

        self.mingyue = board2.copy()
        self.mingyue[7][5] = 1
        self.mingyue_name = '明月'
    
        self.yinyue = board2.copy()
        self.yinyue[7][6] = 1
        self.yinyue_name = '银月'

        self.ming2yue = board2.copy()
        self.ming2yue[8][5] = 1
        self.ming2yue_name = '名月'

        self.xieyue = board2.copy()
        self.xieyue[8][6] = 1
        self.xieyue_name = '斜月'

        self.huiyue = board2.copy()
        self.huiyue[9][5] = 1
        self.huiyue_name = '慧月'
    def random_pick(self):
        return choice([self.shuyue, self.xiyue, self.hanyue, self.canyue,\
            self.huayue, self.jinyue, self.yuyue, self.xinyue, self.qiuyue,\
            self.liuyue, self.shuiyue, self.hengyue, self.xiayue, self.changyue,\
            self.lanyue, self.puyue, self.yunyue, self.ruiyue, self.mingyue,\
            self.yinyue, self.ming2yue, self.xieyue, self.huiyue])
openings = open26()