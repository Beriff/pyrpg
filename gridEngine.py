import random as rd
from os import system
system("color")
system("mode con cols=100 lines=23")

red = "\u001b[31m"
black = "\u001b[30m"
green = "\u001b[32m"
yellow = "\u001b[33m"
blue = "\u001b[34m"
magenta = "\u001b[35m"
cyan = "\u001b[36m"
white = "\u001b[37m"
gray = "\u001b[30;1m"
grey = "\u001b[30;1m"
orange = "\u001b[31;1m"
salad = "\u001b[32;1m"
canary = "\u001b[33;1m"
sea = "\u001b[34;1m"
pink = "\u001b[35;1m"
sky = "\u001b[36;1m"
boldWhite = "\u001b[37;1m"
reset = "\u001b[0m"

class generationError(Exception):
    def __init__(self, txt):
        self.text = txt

class graphicError(Exception):
    def __init__(self, txt):
        self.text = txt

class Object:

    #toolID = 0

    def __init__(self, symbol, color, name, bottomTile, level=0, collision=False):
        self.symbol = symbol
        self.color = color
        self.name = name
        self.level = level
        self.collision = collision
        self.bottomTile = bottomTile
        self.objectId = 0

    def setProperties(self, bottomObject, isFluid=False):
        self.bottomObject = bottomObject
        self.isFluid = isFluid

class Grid:
    grid = []
    gridWidth = None
    gridHeight = None
    biome = None

    def clearGrid(self):
        if self.grid == []:
            return False
        else:
            self.grid = []
            return True

    def monoGenerate(self, fillObject, amount):
        if type(fillObject) is Object:
            for i in range(0, amount):
                self.grid.append(fillObject)
        else:
            raise generationError("Need an object to generate a grid")

    def markup(self, step):
        if self.grid == []:
            raise generationError("Can't markup an empty grid")
        else:
            for i in range(0, len(self.grid)):
                if i % step == 0 and i != 0:
                    self.grid[i] = "\n"

            self.grid.pop(0)

    def multiGenerate(self, amount, objectsLIST):
        for i in range(0, amount):
            self.grid.append(objectsLIST[rd.randint(0, len(objectsLIST) - 1)])

    def setProperties(self):
        if self.grid == []:
            raise generationError("Can't set properties of an empty grid")
        else:
            x = 0

            self.gridHeight = self.grid.count("\n")

            for i in self.grid:
                if type(i) is Object:
                    x += 1
                elif i == "\n":
                    break

            self.gridWidth = x

    def draw(self, mode=0):
        system("cls")
        
        if mode == 0:
            for i in range(0, len(self.grid)):
                if type(self.grid[i]) is Object or type(self.grid[i]) is Player:
                    print(self.grid[i].color + self.grid[i].symbol + reset, end="")
                elif self.grid[i] == "\n":
                    print("\n", end="")
                else:
                    system("cls")
                    raise graphicError("Illegal data in grid! Only objects and new line symbols are allowed!")
        if mode == 1:
            print(self.grid)
        #else:
            #raise graphicError("Wrong drawing mode given.")

class Player:

    exp = 0
    expLimit = None
    expResidue = 0

    standingOn = None
    level = 1

    velocity = 1

    inv = []
    invCapacity = 50
    eq = []

    def __init__(self, hp=100, name="sbeve", symbol="@", color=green):
        self.currentHp = hp
        self.maxHp = hp
        self.name = name
        self.symbol = symbol
        self.color = green

    def isDead(self):
        if self.currentHp <= 0:
            self.currentHp = 0
            return True
        else:
            return False

    def calculateExp(self):
        self.expLimit = abs(self.level * 100)

        if self.exp >= self.expLimit:
            if self.exp > self.expLimit:
                self.expResidue = self.exp - self.expLimit
            
            self.exp = 0 + self.expResidue
            self.level += 1
