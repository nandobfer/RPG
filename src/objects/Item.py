import pygame, init

class Item:
    # name = string, type = 'armor/weapon/ammo', param value
    def __init__(self, name, type, value):
        self.name = name
        self.type = type
        self.value = value


class Weapon(Item):
    def __init__(self, name, type, value):
        super().__init__(name, type, value)

class Ammo(Item):
    def __init__(self, name, type, value):
        super().__init__(name, type, value)

