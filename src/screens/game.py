import pygame, sys, init, conf, Game
from pygame.locals import *
from pygame import mixer
from objects.Button import * # text, size = (width, height), img = string ("path/file.png")
from objects.Creature import * # name, position x, position y, size width, size height
from objects.Item import * # name = string, type = 'armor/weapon/ammo', param value
from objects.Bullet import * # x, y, mouse = (x,y)


def start():
    # create a screen (width,height)
    screen = pygame.display.set_mode(init.resolution, DOUBLEBUF, 16)

    # Background
    background = pygame.image.load('assets/maps/starting.jpg').convert()
    background = pygame.transform.scale(background, (init.resolution[0] * 10, init.resolution[1] * 10))
    map_size = (background.get_width(),background.get_height())
    print(map_size)

    # Player: name, starting position, size, img
    player = Player("Player", init.resolution[0] / 2, init.resolution[1] / 2, 64, 64, conf.player_img)

    # name = string, type = 'armor/weapon/ammo', param value
    pistol = Item("Pistol", "gun", 10)
    player.addItem(pistol, 1)
    player.setWeapon(pistol)
    player.addAmmo(10)

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

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    player.shoot(mouse)

            # Get all keys pressed
            keys = pygame.key.get_pressed()

            # Pause
            if keys[pygame.K_ESCAPE]:
                pause(screen)

        # Move player
        player.move(map_position, map_size, keys)

        # Draw Player
        player.draw(screen)

        # Draw Buttons (screen, mouse)

        for bullet in player.bullets:
            bullet.main(screen)

        # Update Screen
        pygame.display.update()


        # Print mouse coordenates in console
        # print(mouse)

def pause(screen):
    # Background
    pause_background = pygame.Surface(init.resolution, pygame.SRCALPHA)
    pause_background.fill((100, 0, 100, 128))
    screen.blit(pause_background, (0, 0))

    # Quit Button
    quit = Button("Quit", (300, 200), "assets/buttons/button.png")
    quit.setOffset(10, 60)
    quit.setPosition(710, 680)

    # Unpause Button
    unpause = Button("Unpause", (300, 200), "assets/buttons/button.png")
    unpause.setOffset(10, 60)
    unpause.setPosition(375, 680)

    # Pause Menu Flag
    pause = True

    while pause:
        # Getting mouse position = (x,y)
        mouse = pygame.mouse.get_pos()

        # Event Loop
        for event in pygame.event.get():

            # Closing game window
            if event.type == pygame.QUIT:
                quitGame()

            # On mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Quit Button
                if quit.getMouse(mouse):
                    Game.quitGame()
                # Unpause Button
                if unpause.getMouse(mouse):
                    pause = False

        # Draw Buttons (screen, mouse)
        quit.draw(screen, mouse)
        unpause.draw(screen, mouse)

        # Update Screen
        pygame.display.update()


