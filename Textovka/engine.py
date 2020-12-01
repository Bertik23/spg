from colr import color

class RoomAlreadyInGraph(Exception):
    pass

ERRORCOL = (255,0,0)
ROOMCOL = (66, 135, 245)
TEXTCOL = (0,255,255)
DESCRIPTIONCOL = (76, 230, 71)

class Room:
    def __init__(self, id = -1, name="", description="", onEntry="", neighbors=None, accessible = False):
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
        self.items = []

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
        print(color(graph[self.currentRoom].name, fore=DESCRIPTIONCOL, style="bright"))
        print(color(graph[self.currentRoom].description, fore=DESCRIPTIONCOL, style="bright"))
        self.printMoveOptions()

    def printMoveOptions(self):
        out = "Můžeš jít na:"
        for i, neighbor in enumerate(graph[self.currentRoom].neighbors):
            out += f"\n{graph[neighbor].name}"
        print(color(out, fore=TEXTCOL, style="bright"))

    def processCommand(self, command):
        global graph
        commandParts = command.split(" ")
        if commandParts[0] == "go":
            if len(commandParts) >= 2:
                for n in graph[self.currentRoom].neighbors:
                    if graph[n].name == commandParts[1]:
                        self.move(graph[n].id)
                        break
                else:
                    print(color(f"Do {commandParts[1]} nemůžeš jít.", fore=ERRORCOL, style="bright"))
            else:
                print(color("Musíš dodat i místnost.", fore=ERRORCOL))

    def __repr__(self):
        return f"Player"
    def __str__(self):
        return f"Player {self.name}"

class Inventory:
    def __init__(self):
        self.itemsList = []
    def addItem(self, item):
        self.itemsList.append(item)

    @property
    def items(self):
        return self.itemsList

class Item:
    def __init__(self, name="", description=""):
        self.name = name
        self.description = description

def playGame(player: Player):
    playing = True
    print(graph[player.currentRoom].onEntry)
    player.printMoveOptions()
    while playing:
        player.processCommand(input(color(f"{graph[player.currentRoom].name}", fore=ROOMCOL, style="bright")+">"))

graph = Graph()

def setGraph(graphIn):
    global graph
    graph = graphIn