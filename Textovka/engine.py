from colr import color
import unicodedata

import os
import cloudpickle as pickle

import logging

logging.basicConfig(level=logging.DEBUG)


from math import inf

class RoomAlreadyInGraph(Exception):
    pass

class ItemAlreadyInInventory(Exception):
    pass

ERRORCOL = (255,0,0)
ROOMCOL = (66, 135, 245)
TEXTCOL = (0,255,255)
DESCRIPTIONCOL = (76, 230, 71)
WHITE = (255,255,255)
ITEMCOL = (66, 206, 245)
ACTIONCOL = (218, 237, 45)
STORYCOL = (252, 50, 125)

def errorText(text):
    return color(text, fore=ERRORCOL, style="bright")

def text(text):
    return color(text, fore=TEXTCOL, style="bright")

def roomText(text):
    return color(text, fore=ROOMCOL, style="bright")

def descriptionText(text):
    return color(text, fore=DESCRIPTIONCOL, style="bright")

def whiteText(text):
    return color(text, fore=WHITE, style="bright")

def itemText(text):
    return color(text, fore=ITEMCOL, style="bright")

def actionText(text):
    return color(text, fore=ACTIONCOL, style="bright")

def storyText(text):
    return color(text, fore=STORYCOL, style="bright")

def toAscii(s):
    """
    Sanitarize the given unicode string and remove all special/localized
    characters from it.
 
    Category "Mn" stands for Nonspacing_Mark
    """
    try:
        return ''.join(
            c for c in unicodedata.normalize('NFD', s)
            if unicodedata.category(c) != 'Mn'
        )
    except:
        return s

def similar(a,b, minLen = 3):
    """Functions that decides if two strings are similar.

    Curtesy of Vladan Trhlík"""
    if (a.lower() == b[:len(a)].lower() and len(a) >= minLen) or (b.lower() == a[:len(b)].lower() and len(b) >= minLen):
        return True
    return False

def sameFirstChars(a,b):
    for i, character in enumerate(b):
        if a.startswith(b[:i]):
            continue
        else:
            return i-1
    return len(b)

def getMinSimilarLen(l):
    m = 0
    for i,s in enumerate(l):
        if i < len(l)-1:
            for s_ in l:
                if s_ == s:
                    continue
                m = max(m, sameFirstChars(s,s_))

    return m


class Room:
    def __init__(self, id = -1, name="", description="", onEntry="", neighbors=None, accessible = False, items=None, itemsToAccess=None, inspectFunc=None):
        """Room class
        
        Parameters
        ---
        id: :class:`int`
            The id of the room it's accessed with.

        name: :class:`str`
            The name of the room, that will display on entry.

        description: :class:`str`
            The description of the room.

        onEntry: :class:`str`
            The messege that you get on first entry.

        neighbors: :class:`List[int]`
            The list of ids of all neighbors.

        accessible: :class:`bool`
            If the room is accessible at start.
        
        items: :class:`List[Dict]`
            A list of items in the room.
        """
        self.id = id
        self.name = name
        self.description = description
        if neighbors != None:
            self.neighbors = neighbors
        else:
            self.neighbors = []

        self.onEntry = onEntry

        self.accessible = accessible
        self.inventory = Inventory()
        if items != None:
            for item in items:
                self.inventory.addItem(Item(**item))

        self.itemsToAccess = itemsToAccess if itemsToAccess != None else []

        self.entered = False

        self.inspectFunc = eval(inspectFunc) if inspectFunc != None else lambda: ""
        logging.debug(f"Room {self} initiated with {self.__dict__}")

    def onEntryFunc(self, player):
        logging.debug(f"{self}.onEntryFunc({player})")
        for neighbor in self.neighbors:
            i = 0
            for item in graph[neighbor].itemsToAccess:
                if item == -1:
                    break
                if item in player.inventory.itemIds:
                    i += 1
            else:
                if i >= len(graph[neighbor].itemsToAccess):
                    logging.debug(f"{graph[neighbor]}.accessible if currently {graph[neighbor].accessible}")
                    graph[neighbor].accessible = True
                    logging.debug(f"Set {graph[neighbor]}.accessible to True")
                else:
                    logging.debug(f"{graph[neighbor]}.accessible if currently {graph[neighbor].accessible}")
                    graph[neighbor].accessible = False
                    logging.debug(f"Set {graph[neighbor]}.accessible to False")

    def inspect(self):
        print(roomText(self.name)+text(": ")+descriptionText(self.description))
        self.inspectFunc()

    def setAccessibility(self, newAccessibility):
        print(self.accessible)
        self.accessible = newAccessibility
        print(self.accessible)

    def __str__(self):
        return f"{self.name} - {self.description}"

class Graph:
    def __init__(self):
        self.roomsDict = {}
    def addRoom(self, *args, **kvargs):
        """Adds rooms to the graph.
        
        Parameters
        ---
        id: :class:`int`
            The id of the room it's accessed with.

        name: :class:`str`
            The name of the room, that will display on entry.

        description: :class:`str`
            The description of the room.

        onEntry: :class:`str`
            The messege that you get on first entry.

        neighbors: :class:`List[int]`
            The list of ids of all neighbors.
        """
        if args != ():
            id = args[0]
            if len(args) >= 4:
                neighbors = args[4]
            else:
                neighbors = kvargs.get("neighbors")
        else:
            id = kvargs.get("id")
            neighbors = kvargs.get("neighbors")

        if id not in self.roomsDict.keys():
            self.roomsDict[id] = (Room(*args, **kvargs))
        else:
            raise RoomAlreadyInGraph(id)

    def __getitem__(self, item):
        return self.roomsDict[item]

    @property
    def rooms(self):
        for room in self.roomsDict.values():
            yield room

    def __repr__(self):
        return f"Graph({len(self.roomsDict)})"
    def __str__(self):
        out = "Graph\nRooms:"
        for i in self.roomsDict:
            out += f"\n{i.name}"
        return out

class Player:
    def __init__(self, name):
        self.name = name
        self.currentRoom = 0
        self.inventory = Inventory()
    def move(self, room):
        self.currentRoom = room
        graph[self.currentRoom].onEntryFunc(self)
        #print(color(graph[self.currentRoom].name, fore=DESCRIPTIONCOL, style="bright"))
        #print(color(graph[self.currentRoom].description, fore=DESCRIPTIONCOL, style="bright"))
        print(actionText("Přesunul jsi se do ")+roomText(graph[self.currentRoom].name))
        if not graph[self.currentRoom].entered:
            print(storyText(graph[self.currentRoom].onEntry))
            graph[self.currentRoom].entered = True
        self.printMoveOptions()

    def printMoveOptions(self):
        out = text("Můžeš jít na:")
        for i, neighbor in enumerate(graph[self.currentRoom].neighbors):
            out += f"\n{whiteText('•')} {roomText(graph[neighbor].name)}" if graph[neighbor].accessible else ""
        print(out)

    def printVisibleItems(self):
        out = text("Rozhlédl jsi se a vidíš:")
        for item in graph[self.currentRoom].inventory:
            out += f"\n{whiteText('•')} {itemText(item.name)}" if item.visible and not item.destroyed else ""
        print(out)

    def showInventory(self):
        out = text("Tvůj inventář:")
        for item in self.inventory:
            out += f"\n{whiteText('•')} {itemText(item.name)}" if item.visible and not item.destroyed else ""
        print(out)

    def takeItem(self, item, room, makeVisible = True):
        if type(item) == Item:
            if not item.destroyed:
                item.visible = True if makeVisible else item.visible
                self.inventory.addItem(item)
                graph[room].inventory.removeItem(item)
                print(actionText("Vzal jsi ")+itemText(item.name))
                return True
        elif type(item) == int:
            item = graph[room].inventory.getItemById(item)
            if not item.destroyed:
                item.visible = True if makeVisible else item.visible
                self.inventory.addItem(item)
                graph[room].inventory.removeItem(item)
                return True

    def placeItem(self, item, room):
        if type(item) == Item:
            self.inventory.removeItem(item)
            graph[room].inventory.addItem(item)
            print(actionText("Položil jsi ")+itemText(item.name))
        elif type(item) == int:
            item = graph[room].inventory.getItemById(item)
            self.inventory.removeItem(item)
            graph[room].inventory.addItem(item)
        graph[self.currentRoom].onEntryFunc(self)

    def processCommand(self, command):
        global graph
        commandParts = command.split(" ")

        logging.debug(f"Processing Command {command}")

        if similar(commandParts[0], "info"):
            print(descriptionText("Made by ")+itemText("Alber Havliček")+"\n"+descriptionText("Práce zahájena: ")+actionText("1.12.2020 10:00")+"\n"+descriptionText("Práce ukončena: ")+actionText("dd.mm.yyyy hh:mm")+"\n"+descriptionText("Práce vyžadovala: ")+actionText("x hodin."))

        if commandParts[0] == "go":
            if len(commandParts) >= 2:
                for n in graph[self.currentRoom].neighbors:
                    if (similar(graph[n].name.lower(), commandParts[1].lower(), max(getMinSimilarLen([graph[x].name.lower() for x in graph[self.currentRoom].neighbors])+1,3)) or similar(toAscii(graph[n].name.lower()), toAscii(commandParts[1].lower()), max(getMinSimilarLen([toAscii(graph[x].name.lower()) for x in graph[self.currentRoom].neighbors])+1,3))) and graph[n].accessible:
                        self.move(graph[n].id)
                        break
                else:
                    print(errorText("Do ")+roomText(commandParts[1])+errorText(" nemůžeš jít."))
            else:
                print(errorText("Musíš dodat i místnost."))

        if commandParts[0] == "inv":
            self.showInventory()

        if similar(commandParts[0],"look"):
            self.printVisibleItems()

        if similar(commandParts[0],"where"):
            self.printMoveOptions()

        if similar(commandParts[0], "take"):
            if len(commandParts) >= 2:
                for item in graph[self.currentRoom].inventory:
                    if item.visible and item.moveable:
                        if similar(commandParts[1], item.name, max(getMinSimilarLen([x.name.lower() for x in graph[self.currentRoom].inventory]),3)) or similar(toAscii(commandParts[1]), toAscii(item.name), max(getMinSimilarLen([toAscii(x.name.lower()) for x in graph[self.currentRoom].inventory]),3)):
                            self.takeItem(item, self.currentRoom)
                            break
                else:
                    print(itemText(commandParts[1])+errorText(" nemůžeš vzít."))
            else:
                print(errorText("Musíš dodat i předmět."))

        if similar(commandParts[0], "place"):
            if len(commandParts) >= 2:
                for item in self.inventory:
                    if (similar(commandParts[1], item.name, max(getMinSimilarLen([x.name.lower() for x in self.inventory])+1,3)) or similar(toAscii(commandParts[1]), toAscii(item.name), max(getMinSimilarLen([toAscii(x.name.lower()) for x in self.inventory])+1,3))) and item.visible:
                        print(item.visible)
                        self.placeItem(item, self.currentRoom)
                        break
                else:
                    print(itemText(commandParts[1])+errorText(" nemůžeš položit."))
            else:
                print(errorText("Musíš dodat i předmět."))

        if commandParts[0] == "use":
            if len(commandParts) >= 2:
                for item in graph[self.currentRoom].inventory + self.inventory:
                    if item.visible and not item.destroyed:
                        if similar(commandParts[1], item.name, max(getMinSimilarLen([x.name.lower() for x in graph[self.currentRoom].inventory+self.inventory])+1,3)) or similar(toAscii(commandParts[1]), toAscii(item.name), max(getMinSimilarLen([toAscii(x.name.lower()) for x in graph[self.currentRoom].inventory+self.inventory])+1,3)):
                            if not item.use(self, self.currentRoom):
                                print(itemText(commandParts[1])+errorText(" už jsi použil."))
                            break
                else:
                    print(itemText(commandParts[1])+errorText(" nemůžeš použít."))
            else:
                print(errorText("Musíš dodat i předmět."))

        if similar(commandParts[0], "inspect"):
            if len(commandParts) >= 2:
                for item in graph[self.currentRoom].inventory + self.inventory:
                    if item.visible and not item.destroyed:
                        if similar(commandParts[1], item.name, max(getMinSimilarLen([x.name.lower() for x in graph[self.currentRoom].inventory+self.inventory])+1,3)) or similar(toAscii(commandParts[1]), toAscii(item.name), max(getMinSimilarLen([toAscii(x.name.lower()) for x in graph[self.currentRoom].inventory+self.inventory])+1,3)):
                            item.inspect()
                            break
                else:
                    print(itemText(commandParts[1])+errorText(" nemůžeš prohlídnout."))
            else:
                graph[self.currentRoom].inspect()

        if similar(commandParts[0],"save"):
            if len(commandParts) >= 2:
                save = True
                if not os.path.exists("saves"):
                    os.mkdir("saves")
                if os.path.exists(f"saves/{commandParts[1]}.bsav"):
                    overwrite = input(errorText("Save ")+itemText(commandParts[1])+errorText(" už existuje. Chcete ho přepsat? [Y/N] "))
                    while overwrite[0].lower() not in ("y","n","a"):
                        overwrite = input(errorText("Save ")+itemText(commandParts[1])+errorText(" už existuje. Chcete ho přepsat? [Y/N] "))
                    if overwrite[0].lower() in ("y","a"):
                        save = True
                    else:
                        save = False
                if save:
                    with open(f"saves/{commandParts[1]}.bsav","wb") as f:
                        pickle.dump((self, graph), f)
                        print(actionText("Aktuální pozice uložena jako ")+itemText(commandParts[1])+actionText("."))
                else:
                    print(actionText(f"Uložení zrušeno."))
            else:
                print(errorText("Musíš dodat jméno savu."))

        if similar(commandParts[0],"load"):
            if len(commandParts) >= 2:
                if commandParts[1] in [x[:-5] for x in os.listdir("saves")]:
                    with open(f"saves/{commandParts[1]}.bsav","rb") as f:
                        newPlayer, graphA = pickle.load(f)
                        setGraph(graphA)
                        print(actionText("Uložená pozice ")+itemText(commandParts[1])+actionText(" byla načtena."))
                        return False, newPlayer
            else:
                out = errorText("Musíš dodat jméno savu.\n")+text("Savy:")
                for sav in [x[:-5] for x in os.listdir("saves") if x.endswith(".bsav")]:
                    out += whiteText("\n• ")+itemText(sav)
                print(out)

        return True, None


    def __repr__(self):
        return f"Player"
    def __str__(self):
        return f"Player {self.name}"

class Inventory:
    def __init__(self):
        self.itemsDict = {}
    def addItem(self, item):
        if item.id in self.itemsDict.keys():
            raise ItemA
        self.itemsDict[item.id] = item
    def removeItem(self, item):
        del self.itemsDict[item.id]

    @property
    def items(self):
        return list(self.itemsDict.values())
    
    @property
    def itemIds(self):
        return list(self.itemsDict.keys())

    def getItemById(self, id):
        print(self.itemsDict)
        return self.itemsDict[id]

    def __getitem__(self, item):
        return self.items[item]

    def __add__(self, other):
        return self.items + other.items

    def __str__(self):
        return str([str(i) for i in self.items])

class Item:
    def __init__(self, id =-1, name="", description="", visible=True, moveable=True, uses = inf, useFunction=None, onUseFunction=None, destroysWhenUsed = False, inspectFunc=None, onWrongUse=None, onInspectFunc=None, onUseFunctionError=None):
        self.id = id
        self.name = name
        self.description = description
        self.visible = visible
        self.moveable = moveable

        self.uses = uses
        self.useFunction = eval(useFunction) if useFunction != None else lambda x,y: ""
        self.onUseFunction = eval(onUseFunction) if onUseFunction != None else lambda: ""
        self.onWrongUse = eval(onWrongUse) if onWrongUse != None else lambda: ""
        self.onUseFunctionError = eval(onUseFunctionError) if onUseFunctionError != None else lambda: ""

        self.destroysWhenUsed = destroysWhenUsed

        self.inspectFunc = eval(inspectFunc) if inspectFunc != None else lambda: ""
        self.onInspectFunc = eval(onInspectFunc) if onInspectFunc != None else lambda: ""

        self.destroyed = False
        self.inspections = 0

    def use(self, player, room):
        if self.uses >= 1 and not self.destroyed:
            try:
                if self.useFunction(player, room):
                    self.onUseFunction()
                else:
                    self.onWrongUse()
            except:
                self.onUseFunctionError()
            self.uses -= 1
            if self.uses <= 0 and self.destroysWhenUsed:
                self.destroyed = True
            return True
        else:
            return False

    def inspect(self):
        print(itemText(self.name)+text(": ")+descriptionText(self.description))
        if self.inspections <= 0:
            self.inspectFunc()
            self.onInspectFunc()
        self.inspections += 1

    def __str__(self):
        return f"Item({self.name})"

def playGame(player: Player):
    playing = True
    #print(descriptionText(graph[player.currentRoom].onEntry))
    #player.printMoveOptions()
    player.move(player.currentRoom)
    newPlayer = None
    while playing:
        playing, newPlayer = player.processCommand(input(color(f"{graph[player.currentRoom].name}", fore=ROOMCOL, style="bright")+"⮚ "))
    if playing == False and newPlayer != None:
        playGame(newPlayer)


graph = Graph()

def setGraph(graphIn):
    global graph
    graph = graphIn