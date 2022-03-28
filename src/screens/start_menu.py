import pygame, sys
from pygame.locals import *
from pygame import mixer

resolution = (1024, 768)

# Initialize pygame
pygame.init()
# Title and Icon
pygame.display.set_caption("RPG")
# icon = pygame.image.load('player.png')
pygame.display.set_icon(icon)

# create a screen (width,height)
screen = pygame.display.set_mode(resolution, DOUBLEBUF, 16)

def startMenu():
    start_menu = True
    while start_menu:
        screen.fill((25,25,150))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pass

def quit():
    sys.exit()

# Calling start_menu
startMenu()


