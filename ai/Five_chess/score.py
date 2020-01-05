#!/usr/bin/env python
# coding: utf-8

class scores:
    one = 1
    two = 10
    three = 100
    four = 10000
    five = 10000000
    blocked_two = 1
    blocked_three = 10
    blocked_four = 1000

class players:
    com = 1
    hum = 2
    empty = 0
    @staticmethod
    def reverse(Player):
        if Player == 1: return 2
        elif Player == 2: return 1
        else: raise ValueError('reverse P.empty')




