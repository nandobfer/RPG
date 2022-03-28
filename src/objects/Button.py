import pygame, conf

class Button():
    # text, size = (width, height), img = string ("path/file.png")
    def __init__(self, text, size, img):
        self.text = conf.text.render(text, True, (255, 255, 255))
        self.size = size
        self.width = size[0]
        self.height = size[1]
        self.img = pygame.image.load(img).convert_alpha()
        self.offset_x = 0
        self.offset_y = 0

    # set offset for alpha distances in images
    def setOffset(self, x, y):
        self.offset_x = x
        self.offset_y = y

    # mouse = (x, y), position = (x, y)
    def getEvent(self, mouse, position):
        if position[0] <= mouse[0] <= position[0] + self.width and position[1] <= mouse[1] <= position[1] + self.height:
            return True

    # screen, position = (x, y)
    def draw(self, screen, position):
        screen.blit(self.img, (position[0] - self.offset_x, position[1] - self.offset_y))
        screen.blit(self.text, (position[0] + 100, position[1] + 15))

