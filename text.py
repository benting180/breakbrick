import pygame
import parameters as P

# global head_font
pygame.font.init() 
head_font = pygame.font.SysFont(None, 20)

font_large = pygame.font.SysFont(None, 80)


def text_score(score):
    text = f'score: {score:4.0f}'
    text_surface = head_font.render(text, True, P.WHITE)
    return text_surface

def text_fps(dt):
    # text = "fps:" + str(1./dt)
    fps = 1./dt
    text = f'fps: {fps:6.1f}'
    text_surface = head_font.render(text, True, P.WHITE)
    return text_surface

def text_caption():
    text = 'Brick Breaker @@ by benting180"'
    return text

def text_hello_world():
    text = 'Hello World!'
    text_surface = head_font.render(text, True, P.WHITE)
    return text_surface
