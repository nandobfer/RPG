import pygame, init, math
from pygame.locals import *
from pygame import mixer

class Bullet(pygame.sprite.Sprite):
    # x, y, mouse = (x,y)
    def __init__(self, x, y, mouse):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = x+10
        self.rect.centery = y+30

        self.x = x+10
        self.y = y+30
        self.mouse = mouse
        self.speed = 50
        self.angle = math.atan2(y - mouse[1], x - mouse[0])
        self.velocity = [
            math.cos(self.angle) * self.speed,
            math.sin(self.angle) * self.speed
        ]
        self.damage = 0
        self.duration = 0

    # Runs on game loop
    def main(self, screen):
        # bullet boundaries
        if self.x > init.resolution[0] or self.y > init.resolution[1] or (self.x, self.y) < (0,0):
            self.kill()

        # bullet movement
        self.x -= int(self.velocity[0])
        self.y -= int(self.velocity[1])
        self.rect.x = self.x
        self.rect.y = self.y

        # bullet draw >going to be image?
        pygame.draw.circle(screen, (0,0,0), (self.rect.centerx, self.rect.centery), 5)

        # bullet sound
        self.duration += 1
        print(self.duration)

    # enemies = pygame.sprite.Group()
    def getCollision(self, enemies):
        hits = pygame.sprite.spritecollide(self, enemies, False)
        if hits:
            for enemy in hits:
                if enemy.alive:
                    return enemy


            # enemy loses HP

        # collisionSound = mixer.Sound('explosion.wav')
            # collisionSound.play()
            return True

