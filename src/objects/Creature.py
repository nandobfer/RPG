import pygame, init
from src.objects.Item import *
from src.objects.Bullet import *

# General Creature Class
class Creature:
    # name, position x, position y, size width, size height
    def __init__(self, name, x, y, width, height, img):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.move_speed = 5
        self.img = self.img = pygame.image.load(img).convert_alpha()
        self.img = pygame.transform.scale(self.img, (self.width, self.height))
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
    def __init__(self, name, x, y, width, height, img):
        super().__init__(name, x, y, width, height, img)
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
            map[0] -= self.move_speed
            for bullet in self.bullets:
                bullet.x += self.move_speed
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            map[0] += self.move_speed
            for bullet in self.bullets:
                bullet.x -= self.move_speed
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            map[1] -= self.move_speed
            for bullet in self.bullets:
                bullet.y += self.move_speed
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
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
            self.items(append(self.weapon))
        self.weapon = item

    def equipOffhand(self, item):
        self.items.remove(item)
        if self.offhand:
            self.items(append(self.offhand))
        self.offhand = item
        
    def equipHead(self, item):
        self.items.remove(item)
        if self.head:
            self.items(append(self.head))
        self.head = item
        
    def equipChest(self, item):
        self.items.remove(item)
        if self.chest:
            self.items(append(self.chest))
        self.chest = item
        
    def equipLegs(self, item):
        self.items.remove(item)
        if self.legs:
            self.items(append(self.legs))
        self.legs = item
    
    def equipBoots(self, item):
        self.items.remove(item)
        if self.boots:
            self.items(append(self.boots))
        self.boots = item
        
    def equipRing_1(self, item):
        self.items.remove(item)
        if self.ring_1:
            self.items(append(self.ring_1))
        self.ring_1 = item

    def equipRing_2(self, item):
        self.items.remove(item)
        if self.ring_2:
            self.items(append(self.ring_2))
            self.ring_2 = item

    def equipNeck(self, item):
        self.items.remove(item)
        if self.neck:
            self.items(append(self.neck))
        self.neck = item

    def equipBackpack(self, item):
        self.items.remove(item)
        if self.backpack:
            self.items(append(self.backpack))
        self.backpack = item




