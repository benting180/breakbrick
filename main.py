import sys
import time
import math
import pygame

class Wall():
    def __init__(self, x_min, y_min, x_max, y_max):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max
        return

class Brick():
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.x1 = self.x
        self.x2 = self.x + self.w

        self.y1 = self.y
        self.y2 = self.y + self.h

        self.cx = self.x + self.w / 2
        self.cy = self.y + self.h / 2

        self.vortex = [ [self.x         , self.y],
                        [self.x + self.w, self.y],
                        [self.x         , self.y + self.h],
                        [self.x + self.w, self.y + self.h]]
        return

class Seed():
    def __init__(self, x, y, r=10, vx=1, vy=-1):
        self.x = x
        self.y = y
        self.r = r
        self.vx = vx
        self.vy = vy
        self.update()
        self.speed = 500
        return
    
    def update(self):
        self.x1 = self.x - self.r
        self.x2 = self.x + self.r
        self.y1 = self.y - self.r
        self.y2 = self.y + self.r
        return
    
    def nex(self, dt):
        self.x = self.x + self.vx * dt * self.speed
        self.y = self.y + self.vy * dt * self.speed
        self.update()
        return
    
    def flip_vx(self):
        print("flip X")
        self.vx = -self.vx
    
    def flip_vy(self):
        print("flip Y")
        self.vy = -self.vy
    
    def get_cord_int(self):
        return (int(self.x), int(self.y))

class Stand():
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.update()
        return
    
    def update(self):
        self.x1 = self.x
        self.x2 = self.x + self.w
        self.y1 = self.y
        self.y2 = self.y + self.h
        return
    
    def move_left(self, dt):
        self.x = self.x - dt * 500
        self.update()

    def move_right(self, dt):
        self.x = self.x + dt * 500
        self.update()

class Game():
    def __init__(self):
        ## SCORE
        self.score = 0
    
        ## WINDOW
        self.win_w = 800
        self.win_h = 600

        ## COLOR
        self.GREEN = (0, 255, 153)
        self.BLUE = (0, 255, 255)
        self.PINK = (255, 120, 255)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        ## OBJECTS
        self.wall = Wall(0, 0, self.win_w, self.win_h)

        self.bricks = []
        # brick = Brick(600, 100, 100, 40)
        # self.bricks.append(brick)
        for x in range(10, self.win_w-100, 100+10):
            for y in range(10, 150, 40+10):
                brick = Brick(x, y, 100, 40)
                self.bricks.append(brick)

        # self.seeds = []
        seed1 = Seed(500, 500, 10, 1, -1)
        seed2 = Seed(200, 500, 10, -1, -1)
        self.seeds = [seed1, seed2]
        # self.seeds.append(see)

        self.stands = []
        stand = Stand(self.win_w/2, self.win_h-20-10, 150, 20)
        self.stands.append(stand)

        ## INIT
        pygame.init()
        pygame.init()
        self.window_surface = pygame.display.set_mode((self.wall.x_max, self.wall.y_max))
        pygame.display.set_caption('Brick Breaker @@"',)
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
            pygame.draw.rect(self.window_surface, self.GREEN, (b.x, b.y, b.w, b.h), 1)

        for b in self.seeds:
            pygame.draw.circle(self.window_surface, self.PINK, b.get_cord_int(), b.r, 1)

        for s in self.stands:
            pygame.draw.rect(self.window_surface, self.BLUE, (s.x, s.y, s.w, s.h), 1)

        self.update_scoring()
        
    def update(self, dt):
        for s in self.seeds:
            s.nex(dt)
        return

    def collide_wall(self):
        # w/ wall
        remove_i = []
        for i, b in enumerate(self.seeds):
            # if hit the ground , just remove the ball
            # if b.y + b.r > self.wall.y_max:
            #     b.flip_vy()
            if b.y > self.wall.y_max:
                remove_i.append(i)
                print("remove!")
                self.seeds.pop(i)
            if b.x + b.r > self.wall.x_max:
                b.flip_vx()
            if b.x - b.r < self.wall.x_min:
                b.flip_vx()
            if b.y - b.r < self.wall.y_min:
                b.flip_vy()
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
                        s.update()
                        s.flip_vx()

            ## left
            if s.x < b.x1:
                if s.y > b.y1 and s.y < b.y2:
                    if s.x2 > b.x1:
                        hit = True
                        s.x = b.x1-s.r
                        s.update()
                        print("LEFT")
                        s.flip_vx()
            ## down
            if s.y > b.y2:
                if s.x > b.x1 and s.x < b.x2:
                    if s.y1 < b.y2:
                        hit = True
                        s.y = b.y2+s.r
                        s.update()
                        print("DOWN")
                        s.flip_vy()
            ## up
            if s.y < b.y1:
                if s.x > b.x1 and s.x < b.x2:
                    if s.y2 > b.y1:
                        hit = True
                        s.y = b.y1-s.r
                        s.update()
                        print("UP")
                        s.flip_vy()
            
            if hit:
                self.bricks.pop(i)
                self.score_brick()
        return
    def collide_stand(self):
        for st in self.stands:
            for s in self.seeds:
                if s.y2 > st.y1:
                    if s.x2 > st.x1 and s.x1 < st.x2:
                        s.flip_vy()
        return

    def check_endgame(self):
        if len(self.seeds) == 0:
            sys.exit()

        if len(self.bricks) == 0:
            sys.exit()
                    
    def check_collision(self):
        self.collide_wall()
        self.collide_brick()
        self.collide_stand()
        return

    def stand_left(self, dt):
        for st in self.stands:
            st.move_left(dt)
        return
    
    def stand_right(self, dt):
        for st in self.stands:
            st.move_right(dt)
        return
    
    def add_seed(self):
        st = self.stands[0]
        seed1 = Seed(st.x1, st.y-10, 10, -0.5, -1)
        seed2 = Seed(st.x2, st.y-10, 10, +0.5, -1)
        self.seeds.append(seed1)
        self.seeds.append(seed2)
        return
    
    def update_scoring(self):
        text = "score:" + str(self.score)
        text_surface = self.head_font.render(text, True, self.WHITE)
        self.window_surface.blit(text_surface, (10, 10))
        pygame.display.update()



class Menu():
    def __init__(self):
        self.menu_text = ['Play', 'How to Play', 'Setting', 'Ranking', 'Exit']
        self.menu_match = ['gaming', 'tutorial', 'setting', 'ranking', 'exiting']
        self.i = 0
        self.head_font = pygame.font.SysFont(None, 80)
        self.ys = range(150, 400, 60)
        self.xs = [300] * len(self.menu_text)
        return
    
    def select_up(self):
        self.i -= 1
        if self.i < 0:
            self.i = 0
    
    def select_down(self):
        self.i += 1
        if self.i >= len(self.menu_text):
            self.i = len(self.menu_text)-1
    
    def update(self, window_surface):
        window_surface.fill((0, 0, 0))
        
        for j, t in enumerate(self.menu_text):
            text_surface = self.head_font.render(t, True, (255,255,255))
            window_surface.blit(text_surface, (300,  150 + j * 60))
            
        # pygame.draw.circle(window_surface, WHITE, (xs[i], ys[i]), 10, 0)
        pygame.draw.rect(window_surface, (255,255,255), (self.xs[self.i], self.ys[self.i], 400, 60), 1)
        pygame.display.update()
    
    def get_selected(self):
        return self.menu_match[self.i]

game = Game()
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
        menu.update(game.window_surface)

    if mode == 'tutorial':
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    mode = 'menu'

        game.window_surface.fill((0, 0, 0))
        head_font = pygame.font.SysFont(None, 80)
        text_surface1 = head_font.render("use <, >, SPACE to control", True, (255,255,255))
        text_surface2 = head_font.render("press ESC ...", True, (255,255,255))
        game.window_surface.blit(text_surface1, (60,  60))
        game.window_surface.blit(text_surface2, (60, 200))
        pygame.display.update()
        


    if mode == 'gaming':
        keys = pygame.key.get_pressed()  #checking pressed keys
        if keys[pygame.K_LEFT]:
            game.stand_left(dt)
        if keys[pygame.K_RIGHT]:
            game.stand_right(dt)
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    game.add_seed()
                    
        t1 = time.time()
        game.draw()
        pygame.display.update()
        dt = time.time() - t1
        game.update(dt)
        game.check_collision()
        game.check_endgame()

        pygame.event.pump() # process event queue
    
    if mode == 'Exit':
        sys.exit()