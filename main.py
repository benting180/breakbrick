import sys
import time
import math
import random
import pygame

import parameters as P

from shape import Rectangle, MovableRectangle
from shape import Circle, MovableCircle
from shape import Stand

from controller import Controller


def main():
    ctr = Controller()

    while True:
        # print(mode)
        if ctr.mode == 'menu':
            ctr.loop_menu()

        if ctr.mode == 'tutorial':
            ctr.loop_tutorial()

        if ctr.mode == 'gaming':
            ctr.loop_gaming()

        if ctr.mode == 'Exit':
            sys.exit()

if __name__ == '__main__':
    main()