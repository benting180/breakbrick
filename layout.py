import sys
import time
import math
import random
import pygame

import parameters as P

from shape import Rectangle, MovableRectangle
from shape import Circle, MovableCircle, Seed
from shape import Stand

def get_wall(w=P.win_w, h=P.win_h):
    return Rectangle(0, 0, P.win_w, P.win_h)


def get_bricks():
    bricks = []
    for x in range(10, P.win_w-100, 100+10):
        for y in range(10, 150, 40+10):
            brick = Rectangle(x, y, 100, 40)
            bricks.append(brick)
    return bricks

def get_seeds():
    seed1 = Seed(500, 500, 10, 1, -1)
    seed2 = Seed(200, 500, 10, -1, -1)
    return [seed1, seed2]

def get_stands():
    stand = Stand(P.win_w/2, P.win_h-20-10, 150, 20)
    return [stand]
