import pygame, init, conf, random
from src.objects.Item import *
from src.objects.Bullet import *
from pygame.locals import *
from pygame import mixer

# General Creature Class
class Creature(pygame.sprite.Sprite):
    # name, position x, position y, size width, size height
    def __init__(self, name, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill((0,0,255))
        self.image.set_alpha(0)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.move_speed = 0.5
        self.alive = True
        self.max_hp = 50
        self.hp = self.max_hp
        self.hp_bar = pygame.Surface((width, 5))
        self.hp_bar.fill((0,170,0))
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
        self.direction = 'down'
        self.attacking = 0
        self.attack_speed = 1

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

    def healthMain(self, screen):
        if self.alive:
            screen.blit(self.hp_bar, (self.x, self.y - 10))

    def takeDamage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.alive = False
            # self.kill()
        else:
            self.hp_bar = pygame.transform.scale(self.hp_bar, (self.width * self.hp / self.max_hp, 5))

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
        self.ammo_box = pygame.Surface((100, 30))
        self.ammo_txt = conf.small_text.render(str(self.ammo), True, (170, 170, 170))
        self.ammo_box.fill((50,50,50))
        self.inventory_size = 5
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.changed_weapon = False
        self.img_feet_idle = pygame.image.load(f"src/assets/player/Top_Down_Survivor/feet/idle/survivor-idle_0.png")
        self.img_feet_idle = pygame.transform.scale(self.img_feet_idle, (self.width, self.height))
        self.img_body_idle = []
        self.img_body_walking = []
        self.img_feet_walking = []
        for i in range(20):
            self.img_body_idle.append(pygame.image.load(f"src/assets/player/Top_Down_Survivor/handgun/idle/survivor-idle_handgun_{i}.png"))
            self.img_body_walking.append(pygame.image.load(f"src/assets/player/Top_Down_Survivor/handgun/move/survivor-move_handgun_{i}.png"))
            self.img_feet_walking.append(pygame.image.load(f"src/assets/player/Top_Down_Survivor/feet/walk/survivor-walk_{i}.png"))
            self.img_body_idle[i] = pygame.transform.scale(self.img_body_idle[i], (self.width, self.height))
            self.img_body_walking[i] = pygame.transform.scale(self.img_body_walking[i], (self.width, self.height))
            self.img_feet_walking[i] = pygame.transform.scale(self.img_feet_walking[i], (self.width, self.height))
        self.animation_count = 0
        self.move_speed = 2

    # game loop event
    def main(self, screen):
        # updating and drawing health bar
        self.healthMain(screen)
        self.drawAmmoUI(screen)

        # checking if attacking and controling attack speed
        if self.attacking > 0:
            self.attacking -= self.attack_speed
            if self.attacking == 30 and self.equipment['main_hand'].isgun:
                bulletSound = mixer.Sound('src/assets/audio/guns/revolver/clicking.mp3')
                bulletSound.play()


        # animation counting
        if self.animation_count + 1 >= 300:
            self.animation_count = 4
        self.animation_count += 10

        if self.haveWeapon() and self.changed_weapon and self.equipment['main_hand'].name == 'Knife':
            self.changed_weapon = False
            self.img_body_idle = []
            self.img_body_walking = []
            self.img_feet_walking = []
            for i in range(20):
                self.img_body_idle.append(pygame.image.load(f"src/assets/player/Top_Down_Survivor/knife/idle/survivor-idle_knife_{i}.png"))
                self.img_body_walking.append(pygame.image.load(f"src/assets/player/Top_Down_Survivor/knife/move/survivor-move_knife_{i}.png"))
                self.img_feet_walking.append(pygame.image.load(f"src/assets/player/Top_Down_Survivor/feet/walk/survivor-walk_{i}.png"))
                self.img_body_idle[i] = pygame.transform.scale(self.img_body_idle[i], (self.width, self.height))
                self.img_body_walking[i] = pygame.transform.scale(self.img_body_walking[i], (self.width, self.height))
                self.img_feet_walking[i] = pygame.transform.scale(self.img_feet_walking[i], (self.width, self.height))
        elif self.haveWeapon() and self.changed_weapon and self.equipment['main_hand'].name == 'Revolver':
            self.changed_weapon = False
            self.img_body_idle = []
            self.img_body_walking = []
            self.img_feet_walking = []
            for i in range(20):
                self.img_body_idle.append(
                    pygame.image.load(f"src/assets/player/Top_Down_Survivor/handgun/idle/survivor-idle_handgun_{i}.png"))
                self.img_body_walking.append(
                    pygame.image.load(f"src/assets/player/Top_Down_Survivor/handgun/move/survivor-move_handgun_{i}.png"))
                self.img_feet_walking.append(
                    pygame.image.load(f"src/assets/player/Top_Down_Survivor/feet/walk/survivor-walk_{i}.png"))
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
            if self.direction == 'down':
                screen.blit(pygame.transform.rotate(self.img_feet_walking[9], -90), (self.x, self.y))
                screen.blit(pygame.transform.rotate(self.img_body_idle[self.animation_count // 20], -90), (self.x, self.y))
            elif self.direction == 'up':
                screen.blit(pygame.transform.rotate(self.img_feet_walking[9], 90),
                            (self.x, self.y))
                screen.blit(pygame.transform.rotate(self.img_body_walking[self.animation_count // 20], 90),
                            (self.x, self.y))
            elif self.direction == 'right':
                screen.blit(self.img_feet_walking[9], (self.x, self.y))
                screen.blit(self.img_body_walking[self.animation_count // 20], (self.x, self.y))
            else:
                screen.blit(pygame.transform.flip(self.img_feet_walking[9], True, False),
                            (self.x, self.y))
                screen.blit(pygame.transform.flip(self.img_body_walking[self.animation_count // 20], True, False),
                            (self.x, self.y))
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
            self.direction = 'left'
            map[0] -= self.move_speed
            for bullet in self.bullets:
                bullet.x += self.move_speed
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.moving_right = True
            self.direction = 'right'
            map[0] += self.move_speed
            for bullet in self.bullets:
                bullet.x -= self.move_speed
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.moving_up = True
            self.direction = 'up'
            map[1] -= self.move_speed
            for bullet in self.bullets:
                bullet.y += self.move_speed
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.moving_down = True
            self.direction = 'down'
            map[1] += self.move_speed
            for bullet in self.bullets:
                bullet.y -= self.move_speed

        # walking sound

        return True

    # name = string, type = 'armor/weapon/ammo', param value
    def addItem(self, item, quantity):
        for i in range(quantity):
            self.items.append(item)

    def getWeapon(self):
        return self.equipment['main_hand']

    def haveWeapon(self):
        if self.equipment['main_hand']:
            return True

    def getRings(self):
        if self.equipment[l_ring] and self.equipment[r_ring]:
            return 3
        elif self.equipment[l_ring]:
            return 1
        elif self.equipment[r_ring]:
            return 2
        else:
            return 0

    def drawAmmoUI(self, screen):
        weapon = self.getWeapon()
        if weapon:
            if weapon.isgun:
                screen.blit(self.ammo_box, (init.resolution[0] - 120, init.resolution[1] - 50))
                self.ammo_txt = conf.small_text.render(str(self.ammo), True, (170, 170, 170))
                screen.blit(self.ammo_txt, (init.resolution[0] - 80, init.resolution[1] - 45))


    def shoot(self, mouse):
        # if a gun is equipped
        if self.equipment['main_hand'].isgun and self.attacking == 0:
            # if there i ammo
            if self.ammo > 0:
                # instanciate a bullet and adds to sprite group
                bullet = Bullet(self.x, self.y, mouse)
                self.bullets.add(bullet)
                # getting bullet damage from gun's damage
                bullet.damage = self.getWeapon().value
                # removing a bullet
                self.ammo -= 1
                # playing a gunfire sound
                bulletSound = mixer.Sound('src/assets/audio/guns/revolver/fire.wav')
                bulletSound.play()
                # set player direction
                if mouse[0] > self.x and mouse[0] > mouse[1]:
                    self.direction = 'right'
                elif mouse[0] < self.x and mouse[0] < mouse[1]:
                    self.direction = 'left'
                elif mouse[1] > self.y and mouse[1] > mouse[0]:
                    self.direction = 'down'
                elif mouse[1] < self.y and mouse[1] < mouse[0]:
                    self.direction = 'up'

                # flagging attacking for interval control
                self.attacking = 60 * 2

            else:
                bulletSound = mixer.Sound('src/assets/audio/guns/revolver/clicking.mp3')
                bulletSound.play()
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
        self.dead_img = pygame.image.load(f"src/assets/enemies/{name.lower()}_{variant}/dead.png")
        self.dead_img = pygame.transform.scale(self.dead_img, (self.width, self.height))
        self.walk_img = []
        for i in range(16):
            self.walk_img.append(pygame.image.load(f"src/assets/enemies/{name.lower()}_{variant}/skeleton-move_{i + 1}.png"))
            self.walk_img[i] = pygame.transform.scale(self.walk_img[i], (self.width, self.height))
        self.animation_count = 0
        self.reset_offset = 0
        self.offset = (random.randrange(-150,150), random.randrange(-150,150))
        self.target = player
        self.hitbox = 50
        self.last_map = map[:]

    # game loop event
    def main(self, screen, map):
        if not self.alive:
            screen.blit(self.dead_img, (self.x, self.y))
            self.correctPosition(map)
        else:
            self.healthMain(screen)


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
            self.correctPosition(map)

    def correctPosition(self, map):
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


