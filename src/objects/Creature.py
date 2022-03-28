import pygame

# General Creature Class
class Creature():
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
        return (x,y)

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))

class Player(Creature):

    # Scroll the map to make player "move" in opposite direction
    def move(self, map, direction):
        if direction == 'left':
            map[0] -= self.move_speed
        if direction == 'right':
            map[0] += self.move_speed
        if direction == 'up':
            map[1] -= self.move_speed
        if direction == 'down':
            map[1] += self.move_speed

        return True




