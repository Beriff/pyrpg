import gridEngine as ge
import keyboard as kb 
from time import sleep
from random import choice, randint
from os import system
from pynput.keyboard import Key, Controller

#update log that shows latest event
log = None

#for imitating keyborad presses
keyboard = Controller()

#to store all exsisting recipes
creationTabRecipes = []

#player's spawn
playerPosition = 5
#if you're changing that, change markup value too (line 57)
gridSize = 2001

#creating some objects
rock = ge.Object("o", ge.gray, "rock", None)
wood = ge.Object("w", ge.red, "wood", rock, 0, True)
stone_wall = ge.Object("█", ge.white, "stone_wall", rock, 0, True)
sand = ge.Object("▒", ge.yellow, "sand", rock)
sandstone_wall = ge.Object("▓", ge.yellow, "sandstone", rock, 0, True)
grass = ge.Object("o", ge.green, "grass", rock)
sulfur = ge.Object("s", ge.yellow, "sulfur", rock, 0, True)
air = ge.Object("zacwb", ge.black, "air", rock, 0, False, False)
lq_air = ge.Object("zacwb", ge.black, "liquid_air", rock, 0, False, False)

w_chest = ge.Object("x", ge.canary, "wooden_chest", rock, 0, True)
w_chest.objectID = -1
w_chest.inner_storage = []
w_chest.capacity = 100

#creating player
player = ge.Player()
player.standingOn = rock

class Biome:
    
    def __init__(self, name, *surfaceTiles):
        self.biomeSurfaceBlocks = []
        self.biomeDeepBlocks = []
        self.name = name
        for i in surfaceTiles:
            self.biomeSurfaceBlocks.append(i)

    def addDeepTiles(self, *deepTiles):
        for i in deepTiles:
            self.biomeDeepBlocks.append(i)

desert = Biome("desert", sand, sand, sand, sandstone_wall)
plains = Biome("plains", rock, grass, grass, grass, grass, wood)
forest = Biome("forest", grass, grass, wood)
hills = Biome("hills", rock, rock, rock, rock, rock, rock, rock, rock, wood, sulfur)

biomes = [desert, plains, forest, hills]

currentLayerBiome = choice(biomes)

#creating game grid and setting some values of it
grid = ge.Grid()
grid.multiGenerate(gridSize, currentLayerBiome.biomeSurfaceBlocks)
grid.markup(100)
grid.setProperties()
grid.grid[playerPosition] = player

currentGrid = grid
#screen updates when True is in this list
changes = []

#For headstart and pickaxe creating, and fuck loops
player.inv.append(rock)
player.inv.append(rock)
player.inv.append(rock)
player.inv.append(rock)
player.inv.append(wood)
player.inv.append(wood)
player.inv.append(wood)
player.inv.append(wood)

#generally used in "log" and "equipped" labels under game's grid
class emptyObject:
    name = None

empty = emptyObject
player.eq = empty


class Recipe:

    def __init__(self, name, result, reqID, *required):
        self.required = []
        self.name = name
        self.result = result
        self.requiredID = reqID
        for i in required:
            self.required.append(i)

    def craft(self):
        for k in range(0, len(self.required)): #don't ask why i'm using k instead of i here...
            player.inv.remove(self.required[k])

        player.inv.append(self.result)

cooling_cell = ge.Object("o", ge.white, "cooling_cell", rock, 0, True, True)
cooling_cell.objectID = 1
player.inv.append(air)
player.inv.append(cooling_cell)

class Tool:
    def __init__(self, name, toolID, level, durability):
        self.name = name
        self.toolID = toolID #0 - not a tool; 1 - pickaxe; 2 - axe; 3 - shovel; 4 - hoe
        self.level = level
        self.durability = durability

wooden_pickaxe = Tool("wooden_pickaxe", 1, 2, 20)

woodpickRecipe = Recipe("wooden_pickaxe", wooden_pickaxe, 0, wood, rock)
creationTabRecipes.append(woodpickRecipe)
liquidAirrecipe = Recipe("Liquid_Air", lq_air, 1, air)
creationTabRecipes.append(liquidAirrecipe)
w_chestrecipe = Recipe("wooden_chest", w_chest, 0, wood, wood)
creationTabRecipes.append(w_chestrecipe)

#commands at "inventory" tab

isChestNear = False
NorthNear = True
SouthNear = True
EastNear = True
WestNear = True

def userInputDefine(plrInput):
    if plrInput.startswith("eq"): #equip item
        splitted = plrInput.split()
        for i in range(0, len(player.inv)):
            if player.inv[i].name == splitted[1]:
                player.eq = player.inv[i]
                print(player.inv[i].name + " equipped")
                player.inv.pop(i)
                break
    if plrInput.startswith("deq"): #de-equip item
        splitted = plrInput.split()
        if splitted[1] == player.eq.name and player.eq != empty:
            player.inv.append(player.eq)
            player.eq = empty
            print(splitted[1] + " de-equipped")
    if plrInput.startswith("dep-e"): #deposit items to the chest
        try:
            if EastNear:
                splitted = plrInput.split()
                for i in range(0, len(player.inv)):
                    if splitted[1] == player.inv[i].name:
                        currentGrid.grid[playerPosition + 1].inner_storage.append(player.inv[i])
                        player.inv.remove(player.inv[i])
                        print(splitted[1] + " added to east chest")
                        break
            else:
                print("Can't spot east chest")
        except AttributeError:
            print("Tried to access storage of not chest object")
        
    if plrInput.startswith("dep-w"):
        try:
            if WestNear:
                splitted = plrInput.split()
                for i in range(0, len(player.inv)):
                    if splitted[1] == player.inv[i].name:
                        currentGrid.grid[playerPosition - 1].inner_storage.append(player.inv[i])
                        player.inv.remove(player.inv[i])
                        print(splitted[1] + " added to west chest")
                        break
            else:
                print("Can't spot west chest")
        except AttributeError:
            print("Tried to access storage of not chest object")

    if plrInput.startswith("dep-n"):
        try:
            if NorthNear:
                splitted = plrInput.split()
                for i in range(0, len(player.inv)):
                    if splitted[1] == player.inv[i].name:
                        currentGrid.grid[playerPosition - (currentGrid.gridWidth + 1)].inner_storage.append(player.inv[i])
                        player.inv.remove(player.inv[i])
                        print(splitted[1] + " added to north chest")
                        break
            else:
                print("Can't spot north chest")
        except AttributeError:
            print("Tried to access storage of not chest object")

    if plrInput.startswith("dep-s"):
        try:
            if SouthNear:
                splitted = plrInput.split()
                for i in range(0, len(player.inv)):
                    if splitted[1] == player.inv[i].name:
                        currentGrid.grid[playerPosition + (currentGrid.gridWidth + 1)].inner_storage.append(player.inv[i])
                        player.inv.remove(player.inv[i])
                        print(splitted[1] + " added to south chest")
                        break
            else:
                print("Can't spot south chest")
        except AttributeError:
            print("Tried to access storage of not chest object")

    if plrInput.startswith("t-e"):
        try:
            if EastNear:
                splitted = plrInput.split()
                for i in range(0, len(currentGrid.grid[playerPosition + 1].inner_storage)):
                    if splitted[1] == currentGrid.grid[playerPosition + 1].inner_storage[i].name:
                        player.inv.append(currentGrid.grid[playerPosition + 1].inner_storage[i])
                        print("added {0} to your inventory".format(currentGrid.grid[playerPosition + 1].inner_storage[i].name))
                        currentGrid.grid[playerPosition + 1].inner_storage.pop(i)
                        break
            else:
                print("can't spot east chest")
        except AttributeError:
            print("Tried to access storage of not chest object")

    if plrInput.startswith("t-w"):
        try:
            if WestNear:
                splitted = plrInput.split()
                for i in range(0, len(currentGrid.grid[playerPosition - 1].inner_storage)):
                    if splitted[1] == currentGrid.grid[playerPosition - 1].inner_storage[i].name:
                        player.inv.append(currentGrid.grid[playerPosition - 1].inner_storage[i])
                        print("added {0} to your inventory".format(currentGrid.grid[playerPosition - 1].inner_storage[i].name))
                        currentGrid.grid[playerPosition - 1].inner_storage.pop(i)
                        break
            else:
                print("can't spot north chest")
        except AttributeError:
            print("Tried to access storage of not chest object")

    if plrInput.startswith("t-n"):
        try:
            if NorthNear:
                splitted = plrInput.split()
                for i in range(0, len(currentGrid.grid[playerPosition - (currentGrid.gridWidth + 1)].inner_storage)):
                    if splitted[1] == currentGrid.grid[playerPosition - (currentGrid.gridWidth + 1)].inner_storage[i].name:
                        player.inv.append(currentGrid.grid[playerPosition - (currentGrid.gridWidth + 1)].inner_storage[i])
                        print("added {0} to your inventory".format(currentGrid.grid[playerPosition - (currentGrid.gridWidth + 1)].inner_storage[i].name))
                        currentGrid.grid[playerPosition - (currentGrid.gridWidth + 1)].inner_storage.pop(i)
                        break
            else:
                print("can't spot north chest")
        except AttributeError:
            print("Tried to access storage of not chest object")

    if plrInput.startswith("t-s"):
        try:
            if SouthNear:
                splitted = plrInput.split()
                for i in range(0, len(currentGrid.grid[playerPosition + (currentGrid.gridWidth + 1)].inner_storage)):
                    if splitted[1] == currentGrid.grid[playerPosition + (currentGrid.gridWidth + 1)].inner_storage[i].name:
                        player.inv.append(currentGrid.grid[playerPosition + (currentGrid.gridWidth + 1)].inner_storage[i])
                        print("added {0} to your inventory".format(currentGrid.grid[playerPosition + (currentGrid.gridWidth + 1)].inner_storage[i].name))
                        currentGrid.grid[playerPosition + (currentGrid.gridWidth + 1)].inner_storage.pop(i)
                        break
            else:
                print("can't spot south chest")
        except AttributeError:
            print("Tried to access storage of not chest object")
    


            

#showing inventory tab to a player (line 113)
def inventoryTab():
    global isChestNear
    global NorthNear
    global SouthNear
    global EastNear
    global WestNear
    userInput = None
    reservedObjects = []
    nearbyStations = [0]
 
    nearbyStations.append(currentGrid.grid[playerPosition + 1].objectID)
    nearbyStations.append(currentGrid.grid[playerPosition - 1].objectID)
    nearbyStations.append(currentGrid.grid[playerPosition + (currentGrid.gridWidth + 1)].objectID)
    nearbyStations.append(currentGrid.grid[playerPosition - (currentGrid.gridWidth + 1)].objectID)
   

    system("cls")
    print("YOUR INVENTORY. <HELP> FOR A LIST OF COMMANDS")
    print("{0}/{1} SPACE LEFT".format(len(player.inv), player.invCapacity))

    for i in range(0, len(player.inv)):
        if player.inv.count(player.inv[i]) > 1 and not (player.inv[i] in reservedObjects):
            print(player.inv[i].name + " x" + str( player.inv.count( player.inv[i] ) ))
            reservedObjects.append(player.inv[i])
        elif player.inv.count(player.inv[i]) == 1:
            print(player.inv[i].name + " x1")

    if -1 in nearbyStations:
        isChestNear = True
        if nearbyStations.index(-1) == 1:
            EastNear = True
            print("EAST CHEST:")
            for i in currentGrid.grid[playerPosition + 1].inner_storage:
                print(i.name)

        if nearbyStations.index(-1) == 2:
            WestNear = True
            print("WEST CHEST:")
            for i in currentGrid.grid[playerPosition - 1].inner_storage:
                print(i.name)
        if nearbyStations.index(-1) == 3:
            NorthNear = True
            print("SOUTH CHEST:")
            for i in currentGrid.grid[playerPosition + (currentGrid.gridWidth + 1)].inner_storage:
                print(i.name)
        if nearbyStations.index(-1) == 4:
            SouthNear = True
            print("NORTH CHEST:")
            for i in currentGrid.grid[playerPosition - (currentGrid.gridWidth + 1)].inner_storage:
                print(i.name)
    else:
        isChestNear = False

    #keyboard.press(Key.enter)
    userInput = input()
    #keyboard.release(Key.enter)
    while userInput != "e":
        userInputDefine(userInput)
        userInput = input()
    currentGrid.draw(0)

#showing creation tab to a player
def creationTab():
    global playerPosition
    global currentGrid
    nearbyStations = [0]
 
    nearbyStations.append(currentGrid.grid[playerPosition + 1].objectID)
    nearbyStations.append(currentGrid.grid[playerPosition - 1].objectID)
    nearbyStations.append(currentGrid.grid[playerPosition + (currentGrid.gridWidth + 1)].objectID)
    nearbyStations.append(currentGrid.grid[playerPosition - (currentGrid.gridWidth + 1)].objectID)
    system('cls')


    isPossibleToCraft = []
    availableRecipes = []

    print(nearbyStations)
    print("CREATION MENU. \n AVAILABLE BLUEPRINTS:")

    #i hate double loops, they take much more time to understand them
    for i in range(0, len(creationTabRecipes)):
        for j in creationTabRecipes[i].required:
            if j in player.inv and creationTabRecipes[i].requiredID in nearbyStations:
                isPossibleToCraft.append(True)
            else:
                isPossibleToCraft.append(False)

        if not (False in isPossibleToCraft):
            print(creationTabRecipes[i].name)
            availableRecipes.append(creationTabRecipes[i])
        isPossibleToCraft = []

    #defining creation tab commands
    userInput = input()
    while userInput != "q":
        if userInput.startswith("craft"):
            splitted = userInput.split()
            for i in range(0, len(availableRecipes)):
                if splitted[1] == availableRecipes[i].name:
                    availableRecipes[i].craft()
                    print("you crafted {0}!".format(availableRecipes[i].name))

        userInput = input()
    currentGrid.draw(0)

def key_listen():
    global playerPosition
    global changes
    oldPlayerPosition = playerPosition

    #Sorry for big comparing lines. But i think this is the only way, excluding if-else stairs.
    #First condition - if key is pressed
    #Second condition - if player stays near one of 4 borders
    #Third condition - checking if "destination point" haven't any collision

    #The reason why 1 is being added in <S> and <W> movements is preventing player's offset. 

    if kb.is_pressed("s") and not (playerPosition in range( (gridSize - currentGrid.gridWidth), gridSize) ) and (currentGrid.grid[playerPosition + (currentGrid.gridWidth + 1) * player.velocity].collision ==False): 
        changes.append(True)
        newPlayerPosition = playerPosition + (currentGrid.gridWidth + 1) * player.velocity

        currentGrid.grid[oldPlayerPosition] = player.standingOn
        player.standingOn = currentGrid.grid[newPlayerPosition]
        currentGrid.grid[newPlayerPosition] = player
        playerPosition = newPlayerPosition
        sleep(0.1)

    elif kb.is_pressed("w") and not (playerPosition in range(0, currentGrid.gridWidth)) and (currentGrid.grid[ (playerPosition - (currentGrid.gridWidth + 1) * player.velocity) ].collision == False): 
        changes.append(True)
        newPlayerPosition = playerPosition - (currentGrid.gridWidth + 1) * player.velocity 

        currentGrid.grid[oldPlayerPosition] = player.standingOn
        player.standingOn = currentGrid.grid[newPlayerPosition]
        currentGrid.grid[newPlayerPosition] = player
        playerPosition = newPlayerPosition
        sleep(0.1)

    elif kb.is_pressed("d") and ( (playerPosition + 2) % 100 != 0) and (currentGrid.grid[ playerPosition + 1 * player.velocity ].collision == False): 
        changes.append(True)

        newPlayerPosition = playerPosition + 1 * player.velocity

        currentGrid.grid[oldPlayerPosition] = player.standingOn #===================================================================================#
        player.standingOn = currentGrid.grid[newPlayerPosition] #                                                                                   #
        currentGrid.grid[newPlayerPosition] = player            # COPY+PASTE IN ALL MOVEMENT CHECKS. PURPOSE: UPDATING PLAYER'S POSITION ON SCREEN  #
        playerPosition = newPlayerPosition                      #                                                                                   #
        sleep(0.1)                                              #===================================================================================#

    elif kb.is_pressed("a") and ( playerPosition % 100 != 0 ) and (currentGrid.grid[ playerPosition - 1 * player.velocity ].collision == False):
        changes.append(True)

        newPlayerPosition = playerPosition - 1 * player.velocity

        currentGrid.grid[oldPlayerPosition] = player.standingOn
        player.standingOn = currentGrid.grid[newPlayerPosition]
        currentGrid.grid[newPlayerPosition] = player
        playerPosition = newPlayerPosition
        sleep(0.1)

    #TABS OPENING

    elif kb.is_pressed("e"):
        inventoryTab()

    elif kb.is_pressed('q'):
        creationTab()

    #BLOCK BREAKING AND PLACING USING ARROWS
    #almost everything here is ctrl+c ctrl+v
    try:
        global log                                #if obj next to player have collision                    #eq tool type = obj breakability type                           #hit will not go out of grid
        if kb.is_pressed("right arrow") and currentGrid.grid[ playerPosition + 1 ].collision and player.eq.toolID == currentGrid.grid[ playerPosition + 1 ].toolID and ( (playerPosition + 2) % 100 != 0):
            if currentGrid.grid[ playerPosition + 1 ].level < player.eq.level:      #breakable object's level lower than pickaxe's
                if len(player.inv) < player.invCapacity:                            #if inventory isn't full
                    player.inv.append(currentGrid.grid[playerPosition + 1])         #firstly adding item to inventory
                    currentGrid.grid[playerPosition + 1] = currentGrid.grid[playerPosition + 1].bottomTile  #then replacing obj on grid
                else:
                    log = "INVENTORY FULL"
                currentGrid.draw(0) #updating grid
                print("HP {0}/{1}\tLOG: {2}\tEQUIPPED:{3}\tBIOME:{4}".format(player.currentHp, player.maxHp, log, player.eq.name, currentLayerBiome.name)) #and additionally drawing bottom bar

                player.eq.durability -= 1       #lowering pickaxe's (or axe's) durability
                if player.eq.durability <= 0:
                    player.eq = empty
                    log = "PICKAXE BROKE"
        elif kb.is_pressed("right arrow") and not (currentGrid.grid[ playerPosition + 1 ].collision) and player.eq.toolID == 0 and currentGrid.grid[playerPosition + 1] != player.eq: #obj placing mode
            if player.eq.isPlaceable:
                autoreplace = player.eq                 #adding same type obj to equipped, so you can use "rock x4" four times without equipping them every time
                currentGrid.grid[playerPosition + 1] = player.eq
                player.eq = empty
                currentGrid.draw()
                if autoreplace in player.inv:
                    index = player.inv.index(autoreplace)
                    player.eq = player.inv[index]
                    player.inv.pop(index)
            else:
                log = "CAN'T PLACE {0}".format(player.eq.name)


        elif kb.is_pressed("left arrow") and ( playerPosition % 100 != 0 ) and (currentGrid.grid[ playerPosition - 1 ].collision) and player.eq.toolID == 1:
            if currentGrid.grid[ playerPosition - 1 ].level < player.eq.level:
                if len(player.inv) < player.invCapacity:
                    player.inv.append(currentGrid.grid[playerPosition - 1])
                    currentGrid.grid[playerPosition - 1] = currentGrid.grid[playerPosition - 1].bottomTile
                else:
                    log = 'INVENTORY FULL'
                currentGrid.draw(0)
                print("HP {0}/{1}\tLOG: {2}\tEQUIPPED:{3}\tBIOME:{4}".format(player.currentHp, player.maxHp, log, player.eq.name, currentLayerBiome.name))

                player.eq.durability -= 1
                if player.eq.durability <= 0:
                    player.eq = empty
                    log = "PICKAXE BROKE"
        elif kb.is_pressed("left arrow") and ( playerPosition % 100 != 0 ) and not (currentGrid.grid[ playerPosition - 1 ].collision) and player.eq.toolID == 0 and currentGrid.grid[playerPosition + 1] != player.eq:
            if player.eq.isPlaceable:
                autoreplace = player.eq
                currentGrid.grid[playerPosition - 1] = player.eq
                player.eq = empty
                currentGrid.draw()
                if autoreplace in player.inv:
                    index = player.inv.index(autoreplace)
                    player.eq = player.inv[index]
                    player.inv.pop(index)
            else:
                log = "CAN'T PLACE {0}".format(player.eq.name)

        elif kb.is_pressed("up arrow") and not (playerPosition in range(0, currentGrid.gridWidth)) and (currentGrid.grid[ (playerPosition - (currentGrid.gridWidth + 1)) ].collision):
            if currentGrid.grid[ (playerPosition - (currentGrid.gridWidth + 1)) ].level < player.eq.level:
                if len(player.inv) < player.invCapacity:
                    player.inv.append(currentGrid.grid[ (playerPosition - (currentGrid.gridWidth + 1)) ])
                    currentGrid.grid[ (playerPosition - (currentGrid.gridWidth + 1)) ] = currentGrid.grid[ (playerPosition - (currentGrid.gridWidth + 1)) ].bottomTile
                else:
                    log = "INVENTORY FULL"
                currentGrid.draw(0)
                print("HP {0}/{1}\tLOG: {2}\tEQUIPPED:{3}\tBIOME:{4}".format(player.currentHp, player.maxHp, log, player.eq.name, currentLayerBiome.name))

                player.eq.durability -= 1
                if player.eq.durability <= 0:
                    player.eq = empty
                    log = "PICKAXE BROKE"
        elif kb.is_pressed("up arrow") and not (playerPosition in range(0, currentGrid.gridWidth)) and not (currentGrid.grid[ (playerPosition - (currentGrid.gridWidth + 1)) ].collision) and player.eq.toolID == 0 and currentGrid.grid[ (playerPosition - (currentGrid.gridWidth + 1)) ] != player.eq:
            if player.eq.isPlaceable:
                autoreplace = player.eq
                currentGrid.grid[ (playerPosition - (currentGrid.gridWidth + 1)) ] = player.eq
                player.eq = empty
                currentGrid.draw()
                if autoreplace in player.inv:
                    index = player.inv.index(autoreplace)
                    player.eq = player.inv[index]
                    player.inv.pop(index)
            else:
                log = "CAN'T PLACE {0}".format(player.eq.name)

        elif kb.is_pressed("down arrow")  and not (playerPosition in range( (gridSize - currentGrid.gridWidth), gridSize) ) and (currentGrid.grid[playerPosition + (currentGrid.gridWidth + 1)].collision):
            if currentGrid.grid[playerPosition + (currentGrid.gridWidth + 1)].level < player.eq.level:
                if len(player.inv) < player.invCapacity:
                    player.inv.append(currentGrid.grid[playerPosition + (currentGrid.gridWidth + 1)])
                    currentGrid.grid[playerPosition + (currentGrid.gridWidth + 1)] = currentGrid.grid[playerPosition + (currentGrid.gridWidth + 1)].bottomTile
                else:
                    log = "INVENTORY FULL"
                currentGrid.draw(0)
                print("HP {0}/{1}\tLOG: {2}\tEQUIPPED:{3}\tBIOME:{4}".format(player.currentHp, player.maxHp, log, player.eq.name, currentLayerBiome.name))

                player.eq.durability -= 1
                if player.eq.durability <= 0:
                    player.eq = empty
                    log = "PICKAXE BROKE"
        elif kb.is_pressed("down arrow")  and not (playerPosition in range( (gridSize - currentGrid.gridWidth), gridSize) ) and not (currentGrid.grid[playerPosition + (currentGrid.gridWidth + 1)].collision) and player.eq.toolID == 0 and currentGrid.grid[playerPosition + (currentGrid.gridWidth + 1)] != player.eq:
            if player.eq.isPlaceable:
                autoreplace = player.eq
                currentGrid.grid[playerPosition + (currentGrid.gridWidth + 1)] = player.eq
                player.eq = empty
                currentGrid.draw()
                if autoreplace in player.inv:
                    index = player.inv.index(autoreplace)
                    player.eq = player.inv[index]
                    player.inv.pop(index)
            else:
                log = "CAN'T PLACE {0}".format(player.eq.name)

    except AttributeError:
        pass

        
#TODO enemies AI
def physicsCalculate():
    pass

#GAME LOOP
currentGrid.draw(0)
while True:
    previousGrid = currentGrid.grid
    key_listen()
    physicsCalculate()
    #if previousGrid != currentGrid.grid:
    if True in changes:
        currentGrid.draw(0)
        print("HP {0}/{1}\tLOG: {2}\tEQUIPPED:{3}\tBIOME:{4}".format(player.currentHp, player.maxHp, log, player.eq.name, currentLayerBiome.name))
        changes = []
