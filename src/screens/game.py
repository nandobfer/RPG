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
    player = Player("Player", init.resolution[0] / 2, init.resolution[1] / 2, 64, 64)

    # name = string, type = 'armor/weapon/bag_size', param value
    revolver = Item("Revolver", "gun", 10)
    player.addItem(revolver, 1)
    player.equipWeapon(revolver)
    player.addAmmo(100)

    bag = Item("Bag", "backpack", 5)
    player.addItem(bag, 1)
    player.equipBackpack(bag)

    player.addItem(Item("Knife", "weapon", 1), 1)

    # Enemies
    enemies = []
    # name, position x, position y, size width, size height, variant, target
    enemies.append(Enemy("Zombie", player.x, player.y, 64, 64, 3, player))

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
        clock.tick(400)

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

        # Draw enemies
        for enemy in enemies:
            enemy.draw(screen, map_position)

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
        equipment(screen, mouse, player)

        # Update Screen
        pygame.display.update()

        # print(mouse)

def inventory(screen, mouse, player):
    item = []
    size = (64, 64)
    j, k, l = 0, 0, 0
    for i in range(player.backpack.value):
        if i // 5 == 0:
            x = 676 + (64 * i)
            y = 318
            drawFrames(screen, x, y, mouse)
            if i < len(player.items):
                item.append(Slot("", size, player.items[i-1].img))
                item[i-1].setPosition(x, y)
                item[i-1].getItem(player.items[i-1])
                item[i-1].draw(screen, mouse)
        elif i // 5 == 1:
            x = 676 + (64 * j)
            y = 318 + 64
            j += 1
            drawFrames(screen, x, y, mouse)
            if i < len(player.items):
                item.append(Slot("", size, player.items[i-1].img))
                item[i-1].setPosition(x, y)
                item[i-1].draw(screen, mouse)
        elif i // 5 == 2:
            x = 676 + (64 * k)
            y = 318 + 64 + 64
            k += 1
            drawFrames(screen, x, y, mouse)
            if i < len(player.items):
                item.append(Slot("", size, player.items[i-1].img))
                item[i-1].setPosition(x, y)
                item[i-1].draw(screen, mouse)
        elif i // 5 == 3:
            x = 676 + (64 * l)
            y = 318 + 64 + 64 + 64
            l += 1
            drawFrames(screen, x, y, mouse)
            if i < len(player.items):
                item.append(Slot("", size, player.items[i-1].img))
                item[i-1].setPosition(x, y)
                item[i-1].draw(screen, mouse)


def equipment(screen, mouse, player):
    
    drawEquipFrames(screen, mouse)
    drawEquipment(screen, mouse, player)

def drawEquipment(screen, mouse, player):
    size = (64,64)

    # Head
    if not player.head:
        head = Slot("", size, "assets/items/empty_slots/head.png")
    else:
        head = Slot("", size, player.head.img)
    head.setPosition(114, 286)
    head.draw(screen, mouse)

    # Chest
    if not player.chest:
        chest = Slot("", size, "assets/items/empty_slots/chest.png")
    else:
        chest = Slot("", size, player.chest.img)
    chest.setPosition(114, 350)
    chest.draw(screen, mouse)

    # Legs
    if not player.legs:
        legs = Slot("", size, "assets/items/empty_slots/trousers.png")
    else:
        legs = Slot("", size, player.legs.img)
    legs.setPosition(114, 414)
    legs.draw(screen, mouse)

    # Boots
    if not player.boots:
        boots = Slot("", size, "assets/items/empty_slots/feet.png")
    else:
        boots = Slot("", size, player.boots.img)
    boots.setPosition(114, 478)
    boots.draw(screen, mouse)

    # Neck Slot
    if not player.neck:
        neck = Slot("", size, "assets/items/empty_slots/neck.png")
    else:
        neck = Slot("", size, player.neck.img)
    neck.setPosition(50, 318)
    neck.draw(screen, mouse)

    # Backpack Slot
    if not player.backpack:
        backpack = Slot("", size, "assets/items/empty_slots/offhand.png")
    else:
        backpack = Slot("", size, player.backpack.img)
        backpack.setPosition(178, 318)
        backpack.draw(screen, mouse)

    # Weapon Slot
    if not player.weapon:
        weapon = Slot("", size, "assets/items/empty_slots/mainhand.png")
    else:
        weapon = Slot("", size, player.weapon.img)
    weapon.setPosition(50, 382)
    weapon.draw(screen, mouse)

    # Off Hand Slot
    if not player.offhand:
        offhand = Slot("", size, "assets/items/empty_slots/offhand.png")
    else:
        offhand = Slot("", size, player.offhand.img)
    offhand.setPosition(178, 382)
    offhand.draw(screen, mouse)

    # Ring 1 Slot
    if not player.ring_1:
        ring_1 = Slot("", size, "assets/items/empty_slots/ring.png")
    else:
        ring_1 = Slot("", size, player.ring_1.img)
    ring_1.setPosition(50, 446)
    ring_1.draw(screen, mouse)

    # Ring 2 Slot
    if not player.ring_2:
        ring_2 = Slot("", size, "assets/items/empty_slots/ring.png")
    else:
        ring_2 = Slot("", size, player.ring_2.img)
    ring_2.setPosition(178, 446)
    ring_2.draw(screen, mouse)

# draw the equipment frames
def drawEquipFrames(screen, mouse):
    size = (64,64)
    # Empy
    empty_slot = Slot("", size, "assets/items/empty_slots/frame.png")
    # Head
    empty_slot.setPosition(114, 286)
    empty_slot.draw(screen, mouse)
    # Chest
    empty_slot.setPosition(114, 350)
    empty_slot.draw(screen, mouse)
    # Legs
    empty_slot.setPosition(114, 414)
    empty_slot.draw(screen, mouse)
    # Boots
    empty_slot.setPosition(114, 478)
    empty_slot.draw(screen, mouse)
    # Neck
    empty_slot.setPosition(50, 318)
    empty_slot.draw(screen, mouse)
    # Backpack
    empty_slot.setPosition(178, 318)
    empty_slot.draw(screen, mouse)
    # Weapon
    empty_slot.setPosition(50, 382)
    empty_slot.draw(screen, mouse)
    # Off Hand
    empty_slot.setPosition(178, 382)
    empty_slot.draw(screen, mouse)
    # Ring 1
    empty_slot.setPosition(50, 446)
    empty_slot.draw(screen, mouse)
    # Ring 2
    empty_slot.setPosition(178, 446)
    empty_slot.draw(screen, mouse)

# Draw an empty frame
def drawFrames(screen, x, y, mouse):
    size = (64, 64)
    empty_slot = Slot("", size, "assets/items/empty_slots/frame.png")
    empty_slot.setPosition(x, y)
    empty_slot.draw(screen, mouse)