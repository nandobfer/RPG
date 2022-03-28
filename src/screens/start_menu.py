import pygame, sys, init
from pygame.locals import *
from pygame import mixer
from objects.Button import Button # text, size = (width, height)

# create a screen (width,height)
screen = pygame.display.set_mode(init.resolution, DOUBLEBUF, 16)
# Background
background = pygame.image.load('assets/background.jpg').convert()
background = pygame.transform.scale(background, init.resolution)
import conf

def start():
    start_menu = True
    clock = pygame.time.Clock()
    quit = Button("Quit", (100,30), "assets/buttons/button.png")
    quit.setOffset(10, 60)
    while start_menu:
        mouse = pygame.mouse.get_pos()
        clock.tick(10)
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pass

        quit.draw(screen, (710, 680))
        pygame.display.update()
        print(mouse)

def quitGame():
    sys.exit()

# Calling start_menu
# start()


