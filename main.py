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

from menu import Menu

ctr = Controller()
menu = Menu()
mode = 'menu'

while True:
    print(mode)
    if mode == 'menu':
        ## keyboard
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    menu.select_up()
                if e.key == pygame.K_DOWN:
                    menu.select_down()
                if e.key == pygame.K_SPACE:
                    if menu.get_selected() == 'gaming':
                        mode = 'gaming'
                    if menu.get_selected() == 'tutorial':
                        mode = 'tutorial'
                    if menu.get_selected() == 'setting':
                        pass
                    if menu.get_selected() == 'ranking':
                        pass
                    if menu.get_selected() == 'exiting':
                        mode = 'Exit'
        pygame.event.pump() # process event queue
        menu.update(ctr.window)

    if mode == 'tutorial':
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    mode = 'menu'

        ctr.window.fill((0, 0, 0))
        head_font = pygame.font.SysFont(None, 80)
        text_surface1 = head_font.render("use <, >, SPACE to control", True, (255,255,255))
        text_surface2 = head_font.render("press ESC ...", True, (255,255,255))
        ctr.window.blit(text_surface1, (60,  60))
        ctr.window.blit(text_surface2, (60, 200))
        pygame.display.update()
        


    if mode == 'gaming':
        keys = pygame.key.get_pressed()  #checking pressed keys
        if keys[pygame.K_LEFT]:
            ctr.stand_left(dt)
        if keys[pygame.K_RIGHT]:
            ctr.stand_right(dt)
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    ctr.add_seed()
                    
        t1 = time.time()
        ctr.draw_all()
        pygame.display.update()
        dt = time.time() - t1
        ctr.update(dt)
        ctr.check_seed_collision()
        ctr.check_reward_collision()
        ctr.create_rewards()
        ctr.check_endgame()
        ctr.reset_empty()

        pygame.event.pump() # process event queue
    
    if mode == 'Exit':
        sys.exit()