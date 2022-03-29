import pygame, init, conf

class Item:
    # name = string, type = 'armor/weapon/ammo', param value
    def __init__(self, name, type, value):
        self.name = name
        self.type = type
        self.value = value
        self.img = 'assets/items/'+name.lower()+'.png'
        # self.img = pygame.image.load('assets/items/'+name.lower()+'.png').convert_alpha()
        self.slot = None


class Weapon(Item):
    def __init__(self, name, type, value):
        super().__init__(name, type, value)

class Ammo(Item):
    def __init__(self, name, type, value):
        super().__init__(name, type, value)

class Tooltip:
    # name, values
    def __init__(self, name, value):
        self.name = name
        # self.description = description
        self.value = value
        self.img = "assets/buttons/frame.png"
        self.img = pygame.image.load(self.img).convert_alpha()
        self.name_txt = conf.text.render(self.name, True, (170, 170, 170))
        self.value_txt = conf.text.render(str(self.value), True, (170, 170, 170))