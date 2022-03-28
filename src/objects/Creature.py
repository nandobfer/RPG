import pygame, init, conf, random
from src.objects.Item import *
from src.objects.Bullet import *

# General Creature Class
class Creature:
    # name, position x, position y, size width, size height
    def __init__(self, name, x, y, width, height):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.move_speed = 0.5
        # self.img = self.img = pygame.image.load(img).convert_alpha()
        # self.img = pygame.transform.scale(self.img, (self.width, self.height))
        self.level = 1
        self.items = []

    # Returns creature's name
    def getName(self):
        return self.name

    # Sets creature's name as the one in argument
    def setName(self, new_name):
        self.name = new_name

    # Sets creature's level as the one in argument
    def setLevel(self, new_level):
        self.level = new_level

    # Returns creature's level (int)
    def getPosition(self):
        return self.level

    # Returns creature's position as a tuple
    def getPosition(self):
        return (self.x,self.y)

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))

class Player(Creature):
    # name, position x, position y, size width, size height
    def __init__(self, name, x, y, width, height):
        super().__init__(name, x, y, width, height)
        self.bullets = []
        self.ammo = 0
        self.weapon = None
        self.head = None
        self.chest = None
        self.legs = None
        self.boots = None
        self.offhand = None
        self.ring_1 = None
        self.ring_2 = None
        self.neck = None
        self.backpack = None
        self.inventory_size = 5
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.changed_weapon = False
        self.img_feet_idle = pygame.image.load(f"assets/player/Top_Down_Survivor/feet/idle/survivor-idle_0.png")
        self.img_feet_idle = pygame.transform.scale(self.img_feet_idle, (self.width, self.height))
        self.img_body_idle = []
        self.img_body_walking = []
        self.img_feet_walking = []
        for i in range(20):
            self.img_body_idle.append(pygame.image.load(f"assets/player/Top_Down_Survivor/handgun/idle/survivor-idle_handgun_{i}.png"))
            self.img_body_walking.append(pygame.image.load(f"assets/player/Top_Down_Survivor/handgun/move/survivor-move_handgun_{i}.png"))
            self.img_feet_walking.append(pygame.image.load(f"assets/player/Top_Down_Survivor/feet/walk/survivor-walk_{i}.png"))
            self.img_body_idle[i] = pygame.transform.scale(self.img_body_idle[i], (self.width, self.height))
            self.img_body_walking[i] = pygame.transform.scale(self.img_body_walking[i], (self.width, self.height))
            self.img_feet_walking[i] = pygame.transform.scale(self.img_feet_walking[i], (self.width, self.height))
        self.animation_count = 0
        self.move_speed = 2

    def draw(self, screen):
        if self.animation_count + 1 >= 300:
            self.animation_count = 4
        self.animation_count += 10

        if self.changed_weapon and self.weapon.name == 'Knife':
            self.changed_weapon = False
            self.img_body_idle = []
            self.img_body_walking = []
            self.img_feet_walking = []
            for i in range(20):
                self.img_body_idle.append(pygame.image.load(f"assets/player/Top_Down_Survivor/knife/idle/survivor-idle_knife_{i}.png"))
                self.img_body_walking.append(pygame.image.load(f"assets/player/Top_Down_Survivor/knife/move/survivor-move_knife_{i}.png"))
                self.img_feet_walking.append(pygame.image.load(f"assets/player/Top_Down_Survivor/feet/walk/survivor-walk_{i}.png"))
                self.img_body_idle[i] = pygame.transform.scale(self.img_body_idle[i], (self.width, self.height))
                self.img_body_walking[i] = pygame.transform.scale(self.img_body_walking[i], (self.width, self.height))
                self.img_feet_walking[i] = pygame.transform.scale(self.img_feet_walking[i], (self.width, self.height))
        elif self.changed_weapon and self.weapon.name == 'Revolver':
            self.changed_weapon = False
            self.img_body_idle = []
            self.img_body_walking = []
            self.img_feet_walking = []
            for i in range(20):
                self.img_body_idle.append(
                    pygame.image.load(f"assets/player/Top_Down_Survivor/handgun/idle/survivor-idle_handgun_{i}.png"))
                self.img_body_walking.append(
                    pygame.image.load(f"assets/player/Top_Down_Survivor/handgun/move/survivor-move_handgun_{i}.png"))
                self.img_feet_walking.append(
                    pygame.image.load(f"assets/player/Top_Down_Survivor/feet/walk/survivor-walk_{i}.png"))
                self.img_body_idle[i] = pygame.transform.scale(self.img_body_idle[i], (self.width, self.height))
                self.img_body_walking[i] = pygame.transform.scale(self.img_body_walking[i], (self.width, self.height))
                self.img_feet_walking[i] = pygame.transform.scale(self.img_feet_walking[i], (self.width, self.height))

        if self.moving_right:
            screen.blit(self.img_feet_walking[self.animation_count // 20], (self.x, self.y))
            screen.blit(self.img_body_walking[self.animation_count // 20], (self.x, self.y))
        elif self.moving_left:
            screen.blit(pygame.transform.flip(self.img_feet_walking[self.animation_count // 20], True, False), (self.x, self.y))
            screen.blit(pygame.transform.flip(self.img_body_walking[self.animation_count // 20], True, False), (self.x, self.y))
        elif self.moving_up:
            screen.blit(pygame.transform.rotate(self.img_feet_walking[self.animation_count // 20], 90),
                        (self.x, self.y))
            screen.blit(pygame.transform.rotate(self.img_body_walking[self.animation_count // 20], 90),
                        (self.x, self.y))
        elif self.moving_down:
            screen.blit(pygame.transform.rotate(self.img_feet_walking[self.animation_count // 20], -90),
                        (self.x, self.y))
            screen.blit(pygame.transform.rotate(self.img_body_walking[self.animation_count // 20], -90),
                        (self.x, self.y))
        else:
            screen.blit(pygame.transform.rotate(self.img_feet_walking[0], -90), (self.x, self.y))
            screen.blit(pygame.transform.rotate(self.img_body_idle[self.animation_count // 20], -90), (self.x, self.y))
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    # Scroll the map to make player "move" in opposite direction
    def move(self, map, size, keys):

        # Setting player boundaries
        if map[0] <= 0.1 * size[0]:
            map[0] = 0.1 * size[0]
        elif map[0] >= 0.8 * size[0]:
            map[0] = 0.8 * size[0]
        if map[1] <= 0.1 * size[1]:
            map[1] = 0.1 * size[1]
        elif map[1] >= 0.8 * size[1]:
            map[1] = 0.8 * size[1]

        # Moving map
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.moving_left = True
            map[0] -= self.move_speed
            for bullet in self.bullets:
                bullet.x += self.move_speed
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.moving_right = True
            map[0] += self.move_speed
            for bullet in self.bullets:
                bullet.x -= self.move_speed
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.moving_up = True
            map[1] -= self.move_speed
            for bullet in self.bullets:
                bullet.y += self.move_speed
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.moving_down = True
            map[1] += self.move_speed
            for bullet in self.bullets:
                bullet.y -= self.move_speed

        return True

    # name = string, type = 'armor/weapon/ammo', param value
    def addItem(self, item, quantity):
        for i in range(quantity):
            self.items.append(item)

    def getWeapon(self):
        return self.weapon

    def getRings(self):
        if self.ring_1 and self.ring_2:
            return 3
        elif self.ring_1:
            return 1
        elif self.ring_2:
            return 2
        else:
            return 0

    def shoot(self, mouse):
        if self.weapon.type == 'gun':
            if self.ammo > 0:
                self.bullets.append(Bullet(self.x, self.y, mouse))
                self.ammo -= 1
            else:
                # empty gun sound
                pass
    
# EQUIPMENT SETS
    # quantity = int
    def addAmmo(self, quantity):
        self.ammo += quantity

    def equipWeapon(self, item):
        self.items.remove(item)
        if self.weapon:
            self.items.append(self.weapon)
        self.weapon = item
        self.changed_weapon = True

    def equipOffhand(self, item):
        self.items.remove(item)
        if self.offhand:
            self.items.append(self.offhand)
        self.offhand = item
        
    def equipHead(self, item):
        self.items.remove(item)
        if self.head:
            self.items.append(self.head)
        self.head = item
        
    def equipChest(self, item):
        self.items.remove(item)
        if self.chest:
            self.items.append(self.chest)
        self.chest = item
        
    def equipLegs(self, item):
        self.items.remove(item)
        if self.legs:
            self.items.append(self.legs)
        self.legs = item
    
    def equipBoots(self, item):
        self.items.remove(item)
        if self.boots:
            self.items.append(self.boots)
        self.boots = item
        
    def equipRing_1(self, item):
        self.items.remove(item)
        if self.ring_1:
            self.items.append(self.ring_1)
        self.ring_1 = item

    def equipRing_2(self, item):
        self.items.remove(item)
        if self.ring_2:
            self.items.append(self.ring_2)
            self.ring_2 = item

    def equipNeck(self, item):
        self.items.remove(item)
        if self.neck:
            self.items.append(self.neck)
        self.neck = item

    def equipBackpack(self, item):
        self.items.remove(item)
        if self.backpack:
            self.items.append(self.backpack)
        self.backpack = item

class Enemy(Creature):
    # name, position x, position y, size width, size height, variant, target
    def __init__(self, name, x, y, width, height, variant, player):
        super().__init__(name, x, y, width, height)
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.move_speed = 0.5
        self.walk_img = []
        for i in range(16):
            self.walk_img.append(pygame.image.load(f"assets/enemies/{name.lower()}_{variant}/skeleton-move_{i + 1}.png"))
            self.walk_img[i] = pygame.transform.scale(self.walk_img[i], (self.width, self.height))
        self.animation_count = 0
        self.reset_offset = 0
        self.offset = (random.randrange(-150,150), random.randrange(-150,150))
        self.target = player

    def draw(self, screen, map):
        if self.animation_count + 1 >= 256:
             self.animation_count = 0
        self.animation_count += 1

        if self.reset_offset == 0:
            self.offset = (random.randrange(-150, 150), random.randrange(-150, 150))
            self.reset_offset = random.randrange(120,150)
        else:
            self.reset_offset -= 1

        if self.target.x + self.offset[0] > self.x - map[0]:
            self.x += self.move_speed
            self.moving_right = True
        if self.target.x + self.offset[0] < self.x - map[0]:
            self.x -= self.move_speed
            self.moving_left = True

        if self.target.y + self.offset[1] > self.y - map[1]:
            self.y += self.move_speed
            self.moving_up = True
        if self.target.y + self.offset[1] < self.y - map[1]:
            self.y -= self.move_speed
            self.moving_down = True

        if self.moving_right:
            screen.blit(self.walk_img[self.animation_count//16], (self.x - map[0], self.y - map[1]))
        elif self.moving_left:
            screen.blit(pygame.transform.flip(self.walk_img[self.animation_count//16], True, False), (self.x - map[0], self.y - map[1]))
        elif self.moving_up:
            screen.blit(pygame.transform.rotate(self.walk_img[self.animation_count // 16], 90), (self.x - map[0], self.y - map[1]))
        elif self.moving_down:
            screen.blit(pygame.transform.rotate(self.walk_img[self.animation_count // 16], -90), (self.x - map[0], self.y - map[1]))
        else:
            screen.blit(self.walk_img[0], (self.x - map[0], self.y - map[1]))
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

