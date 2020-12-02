from colr import color

from math import inf
class RoomAlreadyInGraph(Exception):
    pass

ERRORCOL = (255,0,0)
ROOMCOL = (66, 135, 245)
TEXTCOL = (0,255,255)
DESCRIPTIONCOL = (76, 230, 71)
WHITE = (255,255,255)
ITEMCOL = (66, 206, 245)
ACTIONCOL = (218, 237, 45)

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

def similar(a,b):
    """Functions that decides if two strings are similar.

    Curtesy of Vladan Trhlík"""
    min_len = 3
    if (a.lower() == b[:len(a)].lower() and len(a) >= min_len) or (b.lower() == a[:len(b)].lower() and len(b) >= min_len):
        return True
    return False

class Room:
    def __init__(self, id = -1, name="", description="", onEntry="", neighbors=None, accessible = False, items=None, itemsToAccess=None):
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

    def onEntryFunc(self, player):
        for neighbor in self.neighbors:
            i = 0
            for item in graph[neighbor].itemsToAccess:
                if item in player.inventory.itemIds:
                    i += 1
            if i >= len(graph[neighbor].itemsToAccess):
                graph[neighbor].accessible = True
            else:
                graph[neighbor].accessible = False

    def __str__(self):
        return f"{self.name}\n{self.description}"

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
        print(color(graph[self.currentRoom].name, fore=DESCRIPTIONCOL, style="bright"))
        print(color(graph[self.currentRoom].description, fore=DESCRIPTIONCOL, style="bright"))
        print(actionText("Přesunul jsi se do ")+roomText(graph[self.currentRoom].name))
        self.printMoveOptions()

    def printMoveOptions(self):
        out = text("Můžeš jít na:")
        for i, neighbor in enumerate(graph[self.currentRoom].neighbors):
            out += f"\n{whiteText('•')} {roomText(graph[neighbor].name)}" if graph[neighbor].accessible else ""
        print(out)

    def printVisibleItems(self):
        out = text("Rozhlédl jsi se a vidíš:")
        for item in graph[self.currentRoom].inventory:
            out += f"\n{whiteText('•')} {itemText(item.name)}" if item.visible else ""
        print(out)

    def showInventory(self):
        out = text("Tvůj inventář:")
        for item in self.inventory:
            out += f"\n{whiteText('•')} {itemText(item.name)}" if item.visible else ""
        print(out)

    def takeItem(self, item, room):
        if type(item) == Item:
            item.visible = True
            self.inventory.addItem(item)
            graph[room].inventory.removeItem(item)
            print(actionText("Vzal jsi ")+itemText(item.name))
        elif type(item) == int:
            item = graph[room].inventory.getItemById(item)
            item.visible = True
            self.inventory.addItem(item)
            graph[room].inventory.removeItem(item)

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

        if similar(commandParts[0], "info"):
            print(descriptionText("Made by ")+itemText("Alber Havliček")+"\n"+descriptionText("Práce zahájena: ")+actionText("1.12.2020 10:00")+"\n"+descriptionText("Práce ukončena: ")+actionText("dd.mm.yyyy hh:mm")+"\n"+descriptionText("Práce vyžadovala: ")+actionText("x hodin."))

        if commandParts[0] == "go":
            if len(commandParts) >= 2:
                for n in graph[self.currentRoom].neighbors:
                    if similar(graph[n].name.lower(), commandParts[1].lower()) and graph[n].accessible:
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
                        if similar(commandParts[1], item.name):
                            self.takeItem(item, self.currentRoom)
                            break
                else:
                    print(itemText(commandParts[1])+errorText(" nemůžeš vzít."))
            else:
                print(errorText("Musíš dodat i předmět."))

        if similar(commandParts[0], "place"):
            if len(commandParts) >= 2:
                for item in self.inventory:
                    if similar(commandParts[1], item.name):
                        self.placeItem(item, self.currentRoom)
                        break
                else:
                    print(itemText(commandParts[1])+errorText(" nemůžeš vzít."))
            else:
                print(errorText("Musíš dodat i předmět."))

        if commandParts[0] == "use":
            if len(commandParts) >= 2:
                for item in graph[self.currentRoom].inventory + self.inventory:
                    if item.visible:
                        if similar(commandParts[1], item.name):
                            item.use(self, self.currentRoom)
                            break
                else:
                    print(itemText(commandParts[1])+errorText(" nemůžeš použít."))
            else:
                print(errorText("Musíš dodat i předmět."))


    def __repr__(self):
        return f"Player"
    def __str__(self):
        return f"Player {self.name}"

class Inventory:
    def __init__(self):
        self.itemsDict = {}
    def addItem(self, item):
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
        return self.itemsDict[id]

    def __getitem__(self, item):
        return self.items[item]

    def __add__(self, other):
        return self.items + other.items

    def __str__(self):
        return str([str(i) for i in self.items])

class Item:
    def __init__(self, id =-1, name="", description="", visible=True, moveable=True, uses = inf, useFunction=None, onUseFunction=None):
        self.id = id
        self.name = name
        self.description = description
        self.visible = visible
        self.moveable = moveable

        self.uses = inf
        self.useFunction = eval(useFunction) if useFunction != None else lambda x,y: ""
        self.onUseFunction = eval(onUseFunction) if onUseFunction != None else lambda: ""

    def use(self, player, room):
        self.useFunction(player, room)
        self.onUseFunction()

    def __str__(self):
        return f"Item({self.name})"

def playGame(player: Player):
    playing = True
    print(descriptionText(graph[player.currentRoom].onEntry))
    player.printMoveOptions()
    while playing:
        player.processCommand(input(color(f"{graph[player.currentRoom].name}", fore=ROOMCOL, style="bright")+"⮚ "))

graph = Graph()

def setGraph(graphIn):
    global graph
    graph = graphIn