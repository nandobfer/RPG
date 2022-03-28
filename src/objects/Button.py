import pygame, conf
from src.objects.Item import *

class Button:
    # text, size = (width, height), img = string ("path/file.png")
    def __init__(self, text, size, img):
        self.text = conf.text.render(text, True, (170, 170, 170))
        self.text_mouse = conf.text.render(text, True, (255, 255, 255))
        self.size = size
        self.width = size[0]
        self.height = size[1]
        self.img = pygame.image.load(img).convert_alpha()
        self.img = pygame.transform.scale(self.img, self.size)
        self.offset_x = 0
        self.offset_y = 0
        self.x = 0
        self.y = 0
        self.position = (0,0)

    # set size
    def setSize(self, x, y):
        self.size = (x,y)
        self.width = x
        self.height = y

    # set offset for alpha distances in images
    def setOffset(self, x, y):
        self.offset_x = x
        self.offset_y = y

    # set position for easy access
    def setPosition(self, x, y):
        self.x = x
        self.y = y
        self.position = (x,y)

    # mouse = (x, y), position = (x, y)
    def getMouse(self, mouse):
        if self.x - self.offset_x <= mouse[0] <= self.x - self.offset_x + self.width and self.y <= mouse[1] <= self.y - 2 * self.offset_y + self.height:
            return True

    # screen, mouse = (x,y)
    def draw(self, screen, mouse):
        screen.blit(self.img, (self.x - self.offset_x, self.y - self.offset_y))
        if self.getMouse(mouse):
            screen.blit(self.text_mouse, (self.x + 100, self.y + 15))
        else:
            screen.blit(self.text, (self.x + 100, self.y + 15))

class Slot(Button):
    # text, size = (width, height), img = string ("path/file.png")
    def __init__(self, text, size, img):
        super().__init__(text, size, img)
        self.img_highlighted = 'assets/items/empty_slots/selected_frame.png'
        self.img_highlighted = pygame.image.load(self.img_highlighted).convert_alpha()
        self.img_highlighted = pygame.transform.scale(self.img_highlighted, self.size)
        self.tooltip = Tooltip("", 0)

    # screen
    def draw(self, screen, mouse):
        tooltip = False
        if self.getMouse(mouse):
            screen.blit(self.img_highlighted, (self.x - self.offset_x, self.y - self.offset_y))
            if self.tooltip.name:
                tooltip = True
                screen.blit(self.tooltip.img, (self.x - 300, self.y))
        else:
            screen.blit(self.img, (self.x - self.offset_x, self.y - self.offset_y))
            if tooltip:
                pause_background = pygame.Surface((self.tooltip.img.get_width(), self.tooltip.img.get_height()), pygame.SRCALPHA)
                pause_background.fill((100, 0, 100, 128))
                screen.blit(pause_background, (self.x - 300, self.y))
                tooltip = False

    def getItem(self, item):
        self.item = item
        # name, value
        self.tooltip = Tooltip(item.name, item.value)
