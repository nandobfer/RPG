# General Creature Class
class Creature():
    # name, position x, position y, size width, size height
    def __init__(self, name, x, y, width, height):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    # Returns creature's name
    def getName(self):
        return self.name

    # Sets creature's name as the one in argument
    def setName(self, new_name):
        self.name = new_name

    # Returns creature's position as a tuple
    def getPosition(self):
        return (x,y)

