import sys
import time
import math
import random
import pygame

import parameters as P
import text

from shape import Rectangle, MovableRectangle
from shape import Circle, MovableCircle, Seed
from shape import Reward
from shape import Stand

import physics


from menu import Menu

import layout

class Controller():
    def __init__(self):
        pygame.init()

        ## OBJECTS
        self._hit_brick_i = []
        self._hit_brick_xy = []
        self._hit_reward = []
        self.wall       = layout.get_wall()
        self.bricks     = layout.get_bricks()
        self.seeds      = layout.get_seeds()
        self.stands     = layout.get_stands()
        self.rewards    = []

        self.score = 0

        ## INIT
        self.window = pygame.display.set_mode((self.wall.x2, self.wall.y2))
        pygame.display.set_caption(text.text_caption())
        pygame.display.update()

        
        self.menu = Menu()
        self.mode = 'menu'
        self.dt = 0.1

    ### COLLISION
    def check_reward_collision(self):
        st = self.stands[0]
        for j, r in enumerate(self.rewards):
            hit = physics.collide_up(r, st)
            if hit:
                self._hit_reward.append(j)
                st.enlong()

    def check_seed_collision(self):
        self.collide_wall()
        self.collide_brick()
        self.collide_stand()
        
    def collide_wall(self):
        # w/ wall
        remove_i = []
        for i, b in enumerate(self.seeds):
            side = physics.collide_boundary(b, self.wall)
            
            if side == 'down':
                # if hit the ground , just remove the ball
                # if b.y + b.r > self.wall.y_max:
                #     b.rebound_y()
                remove_i.append(i)
                print("remove!")
                self.seeds.pop(i)
            if side == 'right':
                b.x = self.wall.x2 - b.r
                b.rebound_x()
            if side == 'left':
                b.x = self.wall.x1 + b.r
                b.rebound_x()
            if side == 'up':
                b.rebound_y()
                b.y = self.wall.y1 + b.r

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
            side = physics.collide_which_side(s, b)

            if side == 'right':
                print("RIGHT")
                s.x = b.x2+s.r
                s.auto_complete()
                s.rebound_x()

            if side == 'left':
                s.x = b.x1-s.r
                s.auto_complete()
                print("LEFT")
                s.rebound_x()

            if side == 'down':
                s.y = b.y2+s.r
                s.auto_complete()
                print("DOWN")
                s.rebound_y()

            if side == 'up':
                s.y = b.y1-s.r
                s.auto_complete()
                print("UP")
                s.rebound_y()
            
            if len(side) > 0:
                xy = self.bricks[i].get_coord()
                self._hit_brick_i.append(i)
                self._hit_brick_xy.append(xy)
                
    
    def collide_stand(self):
        for st in self.stands:
            for s in self.seeds:
                hit = physics.collide_up(s, st)
                if hit:
                    s.y = st.y1 - s.r
                    s.rebound_y()

    ### SCORE
    def update_scoring(self):
        _ = text.text_score(self.score)
        self.window.blit(_, (10, 10))
        _ = text.text_fps(self.dt)
        self.window.blit(_, (10, 40))
        pygame.display.update()
    
    def add_score(self):
        self.score += len(self._hit_brick_i) * 10

    ### WINDOW
    def draw_all(self):
        self.window.fill((0, 0, 0))

        for b in self.bricks:
            pygame.draw.rect(self.window, P.GREEN, b.get_dim(), 1)

        for b in self.seeds:
            pygame.draw.circle(self.window, P.PINK, b.get_coord(), b.r, 1)

        for s in self.stands:
            pygame.draw.rect(self.window, P.BLUE, s.get_dim(), 1)
        
        for r in self.rewards:
            pygame.draw.circle(self.window, r.color, r.get_coord(), r.r, 1)

        self.update_scoring()
        
    ### STATE CHANGE
    def update(self, dt):
        for s in self.seeds: s.nex(dt)
        for r in self.rewards: r.nex(dt) 

    def create_rewards(self):
        for xy in self._hit_brick_xy[::-1]:
            if random.random() > 0.1:
                reward = Reward(xy[0], xy[1], 7, 0, 1)
                self.rewards.append(reward)

    def remove_bricks(self):
        for i in sorted(self._hit_brick_i, reverse=True):
            self.bricks.pop(i)
    
    def remove_rewards(self):
        for j in self._hit_reward[::-1]:
            self.rewards.pop(j)

    def check_endgame(self):
        if len(self.seeds) == 0 : sys.exit()
        if len(self.bricks) == 0 : sys.exit()
    
    def reset_empty(self):
        self._hit_brick_i = []
        self._hit_brick_xy = []
        self._hit_reward = []

    ### CONTROL

    def loop_menu(self):

        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    self.menu.select_up()
                if e.key == pygame.K_DOWN:
                    self.menu.select_down()
                if e.key == pygame.K_SPACE:
                    if self.menu.get_selected() == 'gaming':
                        self.mode = 'gaming'
                    if self.menu.get_selected() == 'tutorial':
                        self.mode = 'tutorial'
                    if self.menu.get_selected() == 'setting':
                        pass
                    if self.menu.get_selected() == 'ranking':
                        pass
                    if self.menu.get_selected() == 'exiting':
                        self.mode = 'Exit'
        pygame.event.pump() # process event queue
        self.menu.update(self.window)

    def loop_tutorial(self):
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self.mode = 'menu'

        self.window.fill((0, 0, 0))
        head_font = pygame.font.SysFont(None, 80)
        text_surface1 = head_font.render("use <, >, SPACE to control", True, (255,255,255))
        text_surface2 = head_font.render("press ESC ...", True, (255,255,255))
        self.window.blit(text_surface1, (60,  60))
        self.window.blit(text_surface2, (60, 200))
        pygame.display.update() 
    
    def loop_gaming(self):
        keys = pygame.key.get_pressed()  #checking pressed keys
        if keys[pygame.K_LEFT]:
            for st in self.stands: st.move_left(self.dt, 10)
        if keys[pygame.K_RIGHT]:
            for st in self.stands: st.move_right(self.dt, P.win_w-10)
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    self.add_seed()
                    
        t1 = time.time()
        self.draw_all()
        pygame.display.update()
        self.dt = time.time() - t1
        self.update(self.dt)
        self.check_seed_collision()
        self.check_reward_collision()
        self.create_rewards()
        self.add_score()
        self.remove_bricks()
        self.remove_rewards()
        self.check_endgame()
        self.reset_empty()

        pygame.event.pump() # process event queue      

    def add_seed(self):
        st = self.stands[0]
        # seed1 = Seed(st.x1, st.y-10, 10, -0.5, -1)
        angle = random.random()*math.pi
        seed2 = Seed(st.cx, st.y-10, 10, math.cos(angle), -math.sin(angle))
        # seed3 = Seed(st.x2, st.y-10, 10, +0.5, -1)
        # self.seeds.append(seed1)
        self.seeds.append(seed2)
        # self.seeds.append(seed3)