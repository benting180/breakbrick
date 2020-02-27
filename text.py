import pygame
import parameters as P

# global head_font
pygame.font.init() 
head_font = pygame.font.SysFont(None, 30)



def text_score(score):
    text = "score:" + str(score)
    text_surface = head_font.render(text, True, P.WHITE)
    return text_surface

def text_caption():
    text = 'Brick Breaker @@ by benting180"'
    return text

def text_hello_world():
    text = 'Hello World!'
    text_surface = head_font.render(text, True, P.WHITE)
    return text_surface
