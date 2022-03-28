import pygame, init

class Item:
    # name = string, type = 'armor/weapon/ammo', param value
    def __init__(self, name, type, value):
        self.name = name
        self.type = type
        if self.type == 'armor':
            self.armor = value
        elif self.type == 'weapon':
            self.damage = value
        elif self.type == 'ammo':
            self.ammo = value


class Weapon(Item):
    def __init__(self, name, type, value):
        super().__init__(name, type, value)