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
    background = pygame.image.load('assets/maps/map1.jpg').convert()
    background = pygame.transform.scale(background, (init.resolution[0] * 3, init.resolution[1] * 3))
    map_size = (background.get_width(),background.get_height())
    print(map_size)

    # Music
    mixer.music.load('assets/audio/game.mp3')
    mixer.music.play(-1)
    mixer.music.set_volume(mixer.music.get_volume() / 2)

    # Player: name, starting position, size, img
    player = Player("Player", init.resolution[0] / 2, init.resolution[1] / 2, 64, 64, conf.player_img)

    # name = string, type = 'armor/weapon/ammo', param value
    revolver = Item("Revolver", "gun", 10)
    player.addItem(revolver, 1)
    player.equipWeapon(revolver)
    player.addAmmo(100)

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
        screen.fill((0, 0, 0))
        screen.blit(background, (-map_position[0], -map_position[1]))
        # screen.blit(player.weapon.img, player.getPosition())

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
                pause(screen, player)

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

def pause(screen, player):
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

        inventory(screen, mouse, player)

        # Update Screen
        pygame.display.update()

        print(mouse)

def inventory(screen, mouse, player):
    
    size = (64,64)
    drawFrames(screen)

# Empty Slots
    # Head
    if not player.head:
        head = Slot("", size, "assets/items/empty_slots/head.png")
    else:
        head = Slot("", size, player.head.img)
    head.setPosition(114, 286)
    head.draw(screen)

    # Chest
    if not player.chest:
        chest = Slot("", size, "assets/items/empty_slots/chest.png")
    else:
        chest = Slot("", size, player.chest.img)
    chest.setPosition(114, 350)
    chest.draw(screen)

    # Legs
    if not player.legs:
        legs = Slot("", size, "assets/items/empty_slots/trousers.png")
    else:
        legs = Slot("", size, player.legs.img)
    legs.setPosition(114, 414)
    legs.draw(screen)

    # Boots
    if not player.boots:
        boots = Slot("", size, "assets/items/empty_slots/feet.png")
    else:
        boots = Slot("", size, player.boots.img)
    boots.setPosition(114, 478)
    boots.draw(screen)

    # Neck Slot
    if not player.neck:
        neck = Slot("", size, "assets/items/empty_slots/neck.png")
    else:
        neck = Slot("", size, player.neck.img)
    neck.setPosition(50, 318)
    neck.draw(screen)

    # Backpack Slot
    # if not player.backpack:
        # backpack = Slot("", size, "assets/items/empty_slots/offhand.png")
    # else:
    #     backpack = Slot("", size, player.packpack.img)
        # backpack.setPosition(178, 382)
        # backpack.draw(screen)

    # Weapon Slot
    if not player.weapon:
        weapon = Slot("", size, "assets/items/empty_slots/mainhand.png")
    else:
        weapon = Slot("", size, player.weapon.img)
    weapon.setPosition(50, 382)
    weapon.draw(screen)

    # Off Hand Slot
    if not player.offhand:
        offhand = Slot("", size, "assets/items/empty_slots/offhand.png")
        offhand.setPosition(178, 382)
        offhand.draw(screen)

    # Ring 1 Slot
    if not player.ring_1:
        ring_1 = Slot("", size, "assets/items/empty_slots/ring.png")
        ring_1.setPosition(50, 446)
        ring_1.draw(screen)

    # Ring 2 Slot
    if not player.ring_2:
        ring_2 = Slot("", size, "assets/items/empty_slots/ring.png")
        ring_2.setPosition(178, 446)
        ring_2.draw(screen)

def drawFrames(screen):
    size = (64,64)
    # Empy
    empty_slot = Slot("", size, "assets/items/empty_slots/frame.png")
    # Head
    empty_slot.setPosition(114, 286)
    empty_slot.draw(screen)
    # Chest
    empty_slot.setPosition(114, 350)
    empty_slot.draw(screen)
    # Legs
    empty_slot.setPosition(114, 414)
    empty_slot.draw(screen)
    # Boots
    empty_slot.setPosition(114, 478)
    empty_slot.draw(screen)
    # Neck
    empty_slot.setPosition(50, 318)
    empty_slot.draw(screen)
    # Backpack
    empty_slot.setPosition(178, 318)
    empty_slot.draw(screen)
    # Weapon
    empty_slot.setPosition(50, 382)
    empty_slot.draw(screen)
    # Off Hand
    empty_slot.setPosition(178, 382)
    empty_slot.draw(screen)
    # Ring 1
    empty_slot.setPosition(50, 446)
    empty_slot.draw(screen)
    # Ring 2
    empty_slot.setPosition(178, 446)
    empty_slot.draw(screen)