import pygame, sys, init, conf, Game
from pygame.locals import *
from pygame import mixer
from objects.Button import * # text, size = (width, height), img = string ("path/file.png")
from objects.Creature import * # name, position x, position y, size width, size height


def start():
    # create a screen (width,height)
    screen = pygame.display.set_mode(init.resolution, DOUBLEBUF, 16)

    # Background
    background = pygame.image.load('assets/maps/starting.jpg').convert()
    background = pygame.transform.scale(background, (init.resolution[0] * 10, init.resolution[1] * 10))
    map_size = (background.get_width(),background.get_height())
    print(map_size)


    player = Player("Player", init.resolution[0] / 2, init.resolution[1] / 2, 64, 64, conf.player_img)

    # On Game Flag
    game = True

    # System Clock
    clock = pygame.time.Clock()

    # move throught map scrolling it
    map_position = [100,100]

    # Game Loop
    while game:
        # Getting mouse position = (x,y)
        mouse = pygame.mouse.get_pos()

        # Refresh Rate - FPS
        clock.tick(60)

        # Show Background
        screen.blit(background, (-map_position[0], -map_position[1]))

        # Event Loop
        for event in pygame.event.get():

            # Closing game window
            if event.type == pygame.QUIT:
                Game.quitGame()

            # Get all keys pressed
            keys = pygame.key.get_pressed()

        # Move player
        player.move(map_position, map_size, keys)

        # Draw Player
        player.draw(screen)

        # Update Screen
        pygame.display.update()

        # Print mouse coordenates in console
        # print(mouse)