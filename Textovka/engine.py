class RoomAlreadyInGraph(Exception):
    pass

class ExceededMaxNeighbors(Exception):
    pass

class Room:
    def __init__(self, id = -1, name="", description="", neighbors=None, accessible = False):
        """Room class
        
        Parameters
        ---
        id: :class:`int`
            The id of the room it's accessed with.

        name: :class:`str`
            The name of the room, that will display on entry.

        description: :class:`str`
            The description of the room.

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

        neighbors: :class:`List[int]`
            The list of ids of all neighbors.
        """
        if args != ():
            id = args[0]
            if len(args) >= 4:
                neighbors = args[3]
            else:
                neighbors = kvargs.get("neighbors")
        else:
            id = kvargs.get("id")
            neighbors = kvargs.get("neighbors")
        
        if len(neighbors) > 4:
            raise ExceededMaxNeighbors

        if id not in self.roomsDict.keys():
            self.roomsDict[id] = (Room(*args, **kvargs))
        else:
            raise RoomAlreadyInGraph

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
        print(graph[self.currentRoom].name)
        print(graph[self.currentRoom].description)
        out = "Můžeš jít na:"
        for i, neighbor in enumerate(graph[self.currentRoom].neighbors):
            out += f"\n{['s','z','j','v'][i]}"
        print(out)

    def processCommand(self, command):
        if command == "s":
            self.move(1)

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
    while playing:
        player.processCommand(input("Command? "))

graph = Graph()

def setGraph(graphIn):
    global graph
    graph = graphIn