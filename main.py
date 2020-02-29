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
            # keys = pygame.key.get_pressed()  #checking pressed keys
            # if keys[pygame.K_LEFT]:
            #     ctr.stand_left(dt)
            # if keys[pygame.K_RIGHT]:
            #     ctr.stand_right(dt)
            # for e in pygame.event.get():
            #     if e.type == pygame.KEYDOWN:
            #         if e.key == pygame.K_SPACE:
            #             ctr.add_seed()
                        
            # t1 = time.time()
            # ctr.draw_all()
            # pygame.display.update()
            # dt = time.time() - t1
            # ctr.update(dt)
            # ctr.check_seed_collision()
            # ctr.check_reward_collision()
            # ctr.create_rewards()
            # ctr.add_score()
            # ctr.remove_bricks()
            # ctr.remove_rewards()
            # ctr.check_endgame()
            # ctr.reset_empty()

            # pygame.event.pump() # process event queue
        
        if ctr.mode == 'Exit':
            sys.exit()

if __name__ == '__main__':
    main()