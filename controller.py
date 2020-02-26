import sys
import time
import math
import random
import pygame

import parameters as P

from shape import Rectangle, MovableRectangle
from shape import Circle, MovableCircle
from shape import Stand

class Controller():
    def __init__(self):
        ## SCORE
        self.score = 0
    

        ## OBJECTS
        self.wall = Rectangle(0, 0, P.win_w, P.win_h)

        self.bricks = []
        # brick = Brick(600, 100, 100, 40)
        # self.bricks.append(brick)
        for x in range(10, P.win_w-100, 100+10):
            for y in range(10, 150, 40+10):
                brick = Rectangle(x, y, 100, 40)
                self.bricks.append(brick)

        # self.seeds = []
        seed1 = MovableCircle(500, 500, 10, 1, -1)
        seed2 = MovableCircle(200, 500, 10, -1, -1)
        self.seeds = [seed1, seed2]
        # self.seeds.append(see)

        self.stands = []
        stand = Stand(P.win_w/2, P.win_h-20-10, 150, 20)
        self.stands.append(stand)
    
        self.rewards = []


        ## INIT
        pygame.init()
        pygame.init()
        self.window_surface = pygame.display.set_mode((self.wall.x2, self.wall.y2))
        pygame.display.set_caption('Brick Breaker @@ by benting180"',)
        self.head_font = pygame.font.SysFont(None, 30)
        text_surface = self.head_font.render('Hello World!', True, (255,255,255))
        self.window_surface.blit(text_surface, (10, 10))
        pygame.display.update()
        return

    def score_brick(self):
        self.score += 10

    def draw(self):
        self.window_surface.fill((0, 0, 0))

        for b in self.bricks:
            pygame.draw.rect(self.window_surface, P.GREEN, b.get_dim(), 1)

        for b in self.seeds:
            pygame.draw.circle(self.window_surface, P.PINK, b.get_coord(), b.r, 1)

        for s in self.stands:
            pygame.draw.rect(self.window_surface, P.BLUE, s.get_dim(), 1)
        
        for r in self.rewards:
            pygame.draw.circle(self.window_surface, P.YELLOW, r.get_coord(), r.r, 1)

        self.update_scoring()
        
    def update(self, dt):
        for s in self.seeds:
            s.nex(dt)

        for r in self.rewards:
            r.nex(dt)

        return
    


    def collide_wall(self):
        # w/ wall
        remove_i = []
        for i, b in enumerate(self.seeds):
            # if hit the ground , just remove the ball
            # if b.y + b.r > self.wall.y_max:
            #     b.rebound_y()
            if b.y > self.wall.y2:
                remove_i.append(i)
                print("remove!")
                self.seeds.pop(i)
            if b.x + b.r > self.wall.x2:
                b.x = self.wall.x2 - b.r
                b.rebound_x()
            if b.x - b.r < self.wall.x1:
                b.x = self.wall.x1 + b.r
                b.rebound_x()
            if b.y - b.r < self.wall.y1:
                b.rebound_y()
                b.y = self.wall.y1 + b.r
        # copy_seeds = self.seeds.copy()
        # for i in remove_i:
        #     print(i)
        #     copy_seeds.pop(i)
        return

    def collide_brick(self):
        for s in self.seeds:
            rs = []
            for b in self.bricks:
                r = math.sqrt((b.cx - s.x)**2 + (b.cy - s.y)**2)
                rs.append(r)
        
            if len(rs) == 0:
                return
            i = rs.index(min(rs))
            b = self.bricks[i]

            ## determine which side
            up, down, left, right = False, False, False, False

            hit = False
            if s.x > b.x2:
                if s.y > b.y1 and s.y < b.y2:
                    if s.x1 < b.x2:
                        hit = True
                        # print(s.x1, b.x2)
                        print("RIGHT")
                        
                        s.x = b.x2+s.r
                        s.auto_complete()
                        s.rebound_x()

            ## left
            if s.x < b.x1:
                if s.y > b.y1 and s.y < b.y2:
                    if s.x2 > b.x1:
                        hit = True
                        s.x = b.x1-s.r
                        s.auto_complete()
                        print("LEFT")
                        s.rebound_x()
            ## down
            if s.y > b.y2:
                if s.x > b.x1 and s.x < b.x2:
                    if s.y1 < b.y2:
                        hit = True
                        s.y = b.y2+s.r
                        s.auto_complete()
                        print("DOWN")
                        s.rebound_y()
            ## up
            if s.y < b.y1:
                if s.x > b.x1 and s.x < b.x2:
                    if s.y2 > b.y1:
                        hit = True
                        s.y = b.y1-s.r
                        s.auto_complete()
                        print("UP")
                        s.rebound_y()
            
            if hit:
                ## create rewards
                self.create_reward(*(self.bricks[i].get_coord()))
                self.bricks.pop(i)
                self.score_brick()
        return
    
    def create_reward(self, x, y):
        if random.random() > 0.1:
            reward = MovableCircle(x, y, 7, 0, 1)
            self.rewards.append(reward)

    def collide_stand(self):
        for st in self.stands:
            for s in self.seeds:
                if s.y2 > st.y1:
                    if s.x2 > st.x1 and s.x1 < st.x2:
                        s.y = st.y1 - s.r
                        s.rebound_y()
        return

    def check_endgame(self):
        if len(self.seeds) == 0:
            sys.exit()

        if len(self.bricks) == 0:
            sys.exit()
                    
    def check_seed_collision(self):
        self.collide_wall()
        self.collide_brick()
        self.collide_stand()
        return
    
    def check_reward_collision(self):
        #  for st in self.stands:
        #     for s in self.seeds:
        #         if s.y2 > st.y1:
        #             if s.x2 > st.x1 and s.x1 < st.x2:
        #                 s.rebound_y()
        st = self.stands[0]
        for j, r in enumerate(self.rewards):
            if r.y2 > st.y1:
                if r.x2 > st.x1 and st.x1 < st.x2:
                    self.rewards.pop(j)
                    st.enlong()

    def stand_left(self, dt):
        for st in self.stands:
            st.move_left(dt, 10)
        return
    
    def stand_right(self, dt):
        for st in self.stands:
            st.move_right(dt, P.win_w-10)
        return
    
    def add_seed(self):
        st = self.stands[0]
        seed1 = MovableCircle(st.x1, st.y-10, 10, -0.5, -1)
        seed2 = MovableCircle(st.x2, st.y-10, 10, +0.5, -1)
        self.seeds.append(seed1)
        self.seeds.append(seed2)
        return
    
    def update_scoring(self):
        text = "score:" + str(self.score)
        text_surface = self.head_font.render(text, True, P.WHITE)
        self.window_surface.blit(text_surface, (10, 10))
        pygame.display.update()