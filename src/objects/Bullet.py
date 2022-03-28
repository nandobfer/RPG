import pygame, init, math

class Bullet:
    # x, y, mouse = (x,y)
    def __init__(self, x, y, mouse):
        self.x = x
        self.y = y
        self.mouse = mouse
        self.speed = 15
        self.angle = math.atan2(y - mouse[1], x - mouse[0])
        self.velocity = [
            math.cos(self.angle) * self.speed,
            math.sin(self.angle) * self.speed
        ]

    def main(self, screen):
        self.x -= int(self.velocity[0])
        self.y -= int(self.velocity[1])

        pygame.draw.circle(screen, (0,0,0), (self.x+10, self.y+30), 5)

