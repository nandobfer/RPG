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

    all_sprites = pygame.sprite.Group()

    # Background
    background = pygame.image.load('assets/maps/map1.jpg').convert()
    background = pygame.transform.scale(background, (init.resolution[0] * 3, init.resolution[1] * 3))
    map_size = (background.get_width(),background.get_height())
    print(map_size)

    # Music
    mixer.music.load('assets/audio/game.mp3')
    mixer.music.play(-1)
    mixer.music.set_volume(mixer.music.get_volume() / 2)

    # move throught map scrolling it
    map_position = [100, 100]

    # Player: name, starting position, size, img
    player = Player("Player", init.resolution[0] / 2, init.resolution[1] / 2, 64, 64)
    all_sprites.add(player)

    # name = string, type = 'armor/weapon/bag_size', param value
    revolver = Item("Revolver", "main_hand", 10, True)
    player.addItem(revolver, 1)
    player.equipItem(revolver)
    player.addAmmo(100)

    bag = Item("Bag", "backpack", 9)
    player.addItem(bag, 2)
    player.equipItem(bag)

    knife = Item("Knife", "main_hand", 1)
    player.addItem(knife, 1)
    # player.equipItem(knife)

    # Enemies
    enemies = pygame.sprite.Group()
    # name, position x, position y, size width, size height, variant, target
    enemies.add(Enemy("Zombie", 1000, 500, 85, 85, 4, player, map_position))
    enemies_refresh_counter = 0


    # On Game Flag
    game = True

    # System Clock
    clock = pygame.time.Clock()

    # Game Loop
    while game:
        # Getting mouse position = (x,y)
        mouse = pygame.mouse.get_pos()

        # Refresh Rate - FPS
        clock.tick(60)

        # Show Background
        screen.fill((0, 0, 0))
        screen.blit(background, (-map_position[0], -map_position[1]))
        # screen.blit(player.equipment['main_hand'].img, player.getPosition())

        # Event Loop
        for event in pygame.event.get():

            # Closing game window
            if event.type == pygame.QUIT:
                Game.quitGame()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    player.shoot(mouse)
                    # player.getEquipment()

            # Get all keys pressed
            keys = pygame.key.get_pressed()

            # Pause
            if keys[pygame.K_ESCAPE]:
                pause(screen, player)

        # Move player
        player.move(map_position, map_size, keys)

        # Draw Sprites
        all_sprites.draw(screen)
        player.bullets.draw(screen)
        enemies.draw(screen)

        for enemy in enemies:
            enemy.move(screen, map_position)
            # check for bullets colliding with enemy
            hit = pygame.sprite.spritecollide(enemy, player.bullets, True)


        for bullet in player.bullets:
            bullet.main(screen)

        # Check colisions
        hits = pygame.sprite.spritecollide(player, enemies, False)


        # Draw Player
        player.draw(screen)

        # Draw Buttons (screen, mouse)

        # for bullet in player.bullets:
        #     bullet.main(screen)
        #     for enemy in enemies:
        #         if bullet.getCollision(enemy):
        #             bullet.x = 10000
        #             enemy.x = 10000
        #             enemy.move_speed = 0
        #             del enemy
        #             print("matou")



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

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                pause = False

            # On mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Quit Button
                if quit.getMouse(mouse):
                    Game.quitGame()
                # Unpause Button
                if unpause.getMouse(mouse):
                    pause = False

            inventory(screen, mouse, player, event)

        # Draw Buttons (screen, mouse)
        quit.draw(screen, mouse)
        unpause.draw(screen, mouse)



        # Update Screen
        pygame.display.update()

        # print(mouse)

# controls inventory UI elements, it's inside event loop
# screen, mouse = (x,y), player, event
def inventory(screen, mouse, player, event):
    # set up equipment ui elements
    equipment(screen, mouse, player, event)
    size = (64, 64)
    #list that will receive positions of empty frames
    frame_position = []
    max_rows = (player.equipment['backpack'].value // 5) + 1

    for rows in range(max_rows):
        for i in range(5):
            x = 676 + (64 * (i - 1))
            y = 318 + (64 * rows)
            # saving each position and drawing slot
            frame_position.append((x,y))
            drawFrames(screen, x, y, mouse)

    # drawing each item from player's inventory
    for item in player.items:
        if item:
            # retrieving position from before list
            position = frame_position.pop(0)
            # instanciating a new Slot, positioning and drawing
            item.slot = Slot("", size, item.img)
            item.slot.setPosition(position[0],position[1])
            item.slot.getTooltip(item)
            item.slot.draw(screen, mouse)
            # On mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                if item.slot.getMouse(mouse):
                    player.equipItem(item)


def equipment(screen, mouse, player, event):

    drawEquipFrames(screen, mouse)
    drawEquipment(screen, mouse, player, event)

def drawEquipment(screen, mouse, player, event):
    size = (64,64)

    # Head
    if not player.equipment['head']:
        head = Slot("", size, "assets/items/empty_slots/head.png")
    else:
        head = Slot("", size, playerequipment['head'].img)
    head.setPosition(114, 286)
    head.draw(screen, mouse)
    if head.getMouse(mouse):
        player.unequipItem(player.equipment['head'])

    # Chest
    if not player.equipment['chest']:
        chest = Slot("", size, "assets/items/empty_slots/chest.png")
    else:
        chest = Slot("", size, player.equipment['chest'].img)
    chest.setPosition(114, 350)
    chest.draw(screen, mouse)

    # Legs
    if not player.equipment['legs']:
        legs = Slot("", size, "assets/items/empty_slots/trousers.png")
    else:
        legs = Slot("", size, player.equipment['legs'].img)
    legs.setPosition(114, 414)
    legs.draw(screen, mouse)

    # Boots
    if not player.equipment['boots']:
        boots = Slot("", size, "assets/items/empty_slots/feet.png")
    else:
        boots = Slot("", size, player.equipment['boots'].img)
    boots.setPosition(114, 478)
    boots.draw(screen, mouse)

    # Neck Slot
    if not player.equipment['neck']:
        neck = Slot("", size, "assets/items/empty_slots/neck.png")
    else:
        neck = Slot("", size, player.equipment['neck'].img)
    neck.setPosition(50, 318)
    neck.draw(screen, mouse)

    # Backpack Slot
    if not player.equipment['backpack']:
        backpack = Slot("", size, "assets/items/empty_slots/offhand.png")
    else:
        backpack = Slot("", size, player.equipment['backpack'].img)
        backpack.setPosition(178, 318)
        backpack.draw(screen, mouse)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if head.getMouse(mouse):
                player.unequipItem(player.equipment['backpack'])


    # Weapon Slot
    if not player.equipment['main_hand']:
        mainhand = Slot("", size, "assets/items/empty_slots/mainhand.png")
    else:
        mainhand = Slot("", size, player.equipment['main_hand'].img)
    mainhand.setPosition(50, 382)
    mainhand.draw(screen, mouse)

    # Off Hand Slot
    if not player.equipment['off_hand']:
        offhand = Slot("", size, "assets/items/empty_slots/offhand.png")
    else:
        offhand = Slot("", size, player.equipment['off_hand'].img)
    offhand.setPosition(178, 382)
    offhand.draw(screen, mouse)

    # Ring 1 Slot
    if not player.equipment['l_ring']:
        l_ring = Slot("", size, "assets/items/empty_slots/ring.png")
    else:
        l_ring = Slot("", size, player.equipment['l_ring'].img)
    l_ring.setPosition(50, 446)
    l_ring.draw(screen, mouse)

    # Ring 2 Slot
    if not player.equipment['r_ring']:
        r_ring = Slot("", size, "assets/items/empty_slots/ring.png")
    else:
        r_ring = Slot("", size, player.equipment['r_ring'].img)
    r_ring.setPosition(178, 446)
    r_ring.draw(screen, mouse)

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