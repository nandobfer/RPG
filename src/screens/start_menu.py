import pygame, sys, init, conf, screens.game, Game
from pygame.locals import *
from pygame import mixer
from objects.Button import Button # text, size = (width, height), img = string ("path/file.png")

def start():
    # create a screen (width,height)
    screen = pygame.display.set_mode(init.resolution, DOUBLEBUF, 16)

    # Music
    mixer.music.load('assets/audio/main_menu.mp3')
    mixer.music.play(-1)
    mixer.music.set_volume(mixer.music.get_volume() / 2)

    # Background
    background = pygame.image.load('assets/background.jpg').convert()
    background = pygame.transform.scale(background, init.resolution)

    # Start Menu Flag
    start_menu = True

    # System Clock
    clock = pygame.time.Clock()

    # Quit Button
    quit = Button("Quit", (300,200), "assets/buttons/button.png")
    quit.setOffset(10, 60)
    quit.setPosition(710, 680)

    # Play Button
    play = Button("Play", (300,200), "assets/buttons/button.png")
    play.setOffset(10,60)
    play.setPosition(375, 680)

    # Game Loop
    while start_menu:

        # Getting mouse position = (x,y)
        mouse = pygame.mouse.get_pos()

        # Refresh Rate - FPS
        clock.tick(60)

        # Show Background
        screen.blit(background, (0, 0))

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
                # Play Button
                if play.getMouse(mouse):
                    screens.game.start()
                    mixer.music.stop()
                    start_menu = False

        # Draw Buttons (screen, mouse)
        quit.draw(screen, mouse)
        play.draw(screen, mouse)

        # Update Screen
        pygame.display.update()

        # Print mouse coordenates in console
        # print(mouse)



