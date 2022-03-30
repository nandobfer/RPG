import pygame, init, math

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
        self.speed = 30
        self.angle = math.atan2(y - mouse[1], x - mouse[0])
        self.velocity = [
            math.cos(self.angle) * self.speed,
            math.sin(self.angle) * self.speed
        ]

    def main(self, screen):
        self.x -= int(self.velocity[0])
        self.y -= int(self.velocity[1])
        self.rect.x = self.x
        self.rect.y = self.y

        # pygame.draw.circle(screen, (0,0,0), (self.x, self.y), 5)

    def getCollision(self, enemy):
        distance = math.sqrt(math.pow(enemy.x - self.x, 2) + math.pow(enemy.y - self.y, 2))
        if distance < enemy.hitbox:
            # collisionSound = mixer.Sound('explosion.wav')
            # collisionSound.play()
            return True

