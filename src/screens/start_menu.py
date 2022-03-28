import pygame, sys, init
from pygame.locals import *
from pygame import mixer

# create a screen (width,height)
screen = pygame.display.set_mode(init.resolution, DOUBLEBUF, 16)

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


