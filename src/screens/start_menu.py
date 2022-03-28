import pygame, sys, init
from pygame.locals import *
from pygame import mixer
from objects.Button import Button # text, size = (width, height), img = string ("path/file.png")

# create a screen (width,height)
screen = pygame.display.set_mode(init.resolution, DOUBLEBUF, 16)

# Background
background = pygame.image.load('assets/background.jpg').convert()
background = pygame.transform.scale(background, init.resolution)
import conf

def start():
    # Start Menu Flag
    start_menu = True

    # System Clock
    clock = pygame.time.Clock()

    # Quit Button
    quit = Button("Quit", (300,200), "assets/buttons/button.png")
    quit.setOffset(10, 60)
    quit.setPosition(710, 680)

    # Game Loop
    while start_menu:

        # Getting mouse position = (x,y)
        mouse = pygame.mouse.get_pos()

        # Refresh Rate - FPS
        clock.tick(10)

        # Show Background
        screen.blit(background, (0, 0))

        # Start listening for events
        for event in pygame.event.get():

            # Closing game window
            if event.type == pygame.QUIT:
                quitGame()

            # On mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Quit Button
                if quit.getMouse(mouse):
                    quitGame()

        # Draw Buttons
        quit.draw(screen, mouse)

        # Update Screen
        pygame.display.update()

        # Print mouse coordenates in console
        print(mouse)

def quitGame():
    sys.exit()



