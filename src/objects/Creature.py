import pygame, init, conf, random
from src.objects.Item import *
from src.objects.Bullet import *

# General Creature Class
class Creature(pygame.sprite.Sprite):
    # name, position x, position y, size width, size height
    def __init__(self, name, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill((0,0,255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

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
        self.equipment = {
            'main_hand': None,
            "off_hand": None,
            'head': None,
            'chest': None,
            'legs': None,
            'boots': None,
            'neck': None,
            'backpack': None,
            'l_ring': None,
            'r_ring': None

        }

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
    def getLevel(self):
        return self.level

    # Returns creature's position as a tuple
    def getPosition(self):
        return (self.x,self.y)

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))

    def getEquipment(self):
        for item in self.equipment:
            if self.equipment[item]:
                print(self.equipment[item].name)

class Player(Creature):
    # name, position x, position y, size width, size height
    def __init__(self, name, x, y, width, height):
        super().__init__(name, x, y, width, height)
        self.bullets = pygame.sprite.Group()
        self.ammo = 0
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

        if self.changed_weapon and self.equipment['main_hand'].name == 'Knife':
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
        elif self.changed_weapon and self.equipment['main_hand'].name == 'Revolver':
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
        return self.equipment['main_hand']

    def getRings(self):
        if self.equipment[l_ring] and self.equipment[r_ring]:
            return 3
        elif self.equipment[l_ring]:
            return 1
        elif self.equipment[r_ring]:
            return 2
        else:
            return 0

    def shoot(self, mouse):
        if self.equipment['main_hand'].isgun:
            if self.ammo > 0:
                bullet = Bullet(self.x, self.y, mouse)
                self.bullets.add(bullet)
                self.ammo -= 1
            else:
                # empty gun sound
                pass
    
# EQUIPMENT SETS
    def equipItem(self, item):
        self.items.remove(item)
        if self.equipment[item.type]:
            self.items.append(self.equipment[item.type])
            if item.type == 'main_hand':
                self.changed_weapon = True
        self.equipment[item.type] = item

    def unequipItem(self, item):
        if self.equipment[item.type]:
            self.items.append(self.equipment[item.type])
            if item.type == 'main_hand':
                self.changed_weapon = True
            self.equipment[item.type] = None

    # quantity = int
    def addAmmo(self, quantity):
        self.ammo += quantity

class Enemy(Creature):
    # name, position x, position y, size width, size height, variant, target
    def __init__(self, name, x, y, width, height, variant, player, map):
        super().__init__(name, x, y, width, height)
        self.image.fill((255, 0, 0))
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
        self.hitbox = 50
        self.last_map = map[:]

    def move(self, screen, map):
        if self.animation_count + 1 >= 256:
             self.animation_count = 0
        self.animation_count += 1

        if self.reset_offset == 0:
            self.offset = (random.randrange(-150, 150), random.randrange(-150, 150))
            self.reset_offset = random.randrange(120,150)
        else:
            self.reset_offset -= 1

        if self.target.x + self.offset[0] > self.x:
            self.x += self.move_speed
            self.moving_right = True
        if self.target.x + self.offset[0] < self.x:
            self.x -= self.move_speed
            self.moving_left = True

        if self.target.y + self.offset[1] > self.y:
            self.y += self.move_speed
            self.moving_up = True
        if self.target.y + self.offset[1] < self.y:
            self.y -= self.move_speed
            self.moving_down = True

        if self.moving_right:
            screen.blit(self.walk_img[self.animation_count//16], (self.x, self.y))
        elif self.moving_left:
            screen.blit(pygame.transform.flip(self.walk_img[self.animation_count//16], True, False), (self.x, self.y))
        elif self.moving_up:
            screen.blit(pygame.transform.rotate(self.walk_img[self.animation_count // 16], 90), (self.x, self.y))
        elif self.moving_down:
            screen.blit(pygame.transform.rotate(self.walk_img[self.animation_count // 16], -90), (self.x, self.y))
        else:
            screen.blit(self.walk_img[0], (self.x, self.y))
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        if not self.last_map[0] == map[0]:
            if self.last_map[0] > map[0]:
                self.x += self.last_map[0] - map[0]
            else:
                self.x += self.last_map[0] - map[0]
            self.last_map[0] = map[0]
        if not self.last_map[1] == map[1]:
            if self.last_map[1] > map[1]:
                self.y += self.last_map[1] - map[1]
            else:
                self.y += self.last_map[1] - map[1]
            self.last_map[1] = map[1]
        self.rect.x = self.x
        self.rect.y = self.y



