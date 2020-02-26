import sys
import time
import math
import random
import pygame

import parameters as P

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