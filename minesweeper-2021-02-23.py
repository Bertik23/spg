from tkinter import Tk, Canvas
import typing
import random
import time

SIZE = (600, 600)
BLACK = "black"  # "#000"
WHITE = "white"  # "#FFF"
GREY = "grey"  # "#323232"
LIGHT_GREY = "green"  # "#787878"
MID_GREY = "red"  # "#5F5F5F"

playSize = (10, 10)

display = Tk()
display.title("Mines")
canvas = Canvas(display, width=SIZE[0], height=SIZE[1])
canvas.pack()


class Cell:
    def __init__(self, x, y, type, graph):
        self.x, self.y, self.type = x, y, type
        self.discovered = False
        self.canvasObj = None
        self.clicked = False
        self.graph = graph
        self.flag = None
        self.mouseHover = False

    def draw(self, display: Canvas, gridSize):
        self.gridSize = gridSize
        dSize = [display.winfo_width(), display.winfo_height()]
        t = None
        if not self.discovered:
            if self.mouseHover:
                color = MID_GREY
            else:
                color = GREY
        else:
            mines = self.getMineNeighbors()
            if mines > 0:
                t = str(mines)
            color = LIGHT_GREY
        if self.flag is not None:
            t = self.flag
        if self.canvasObj is None:
            self.canvasObj = display.create_rectangle(
                self.x*dSize[0]//gridSize[0],
                self.y*dSize[1]//gridSize[1],
                (self.x+1)*dSize[0]//gridSize[0],
                (self.y+1)*dSize[1]//gridSize[1],
                fill=color)
        else:
            # print(type(self.canvasObj))
            display.itemconfig(self.canvasObj, fill=color)
            print(color)
            # display.update()
        # print(dir(self.canvasObj))
        if t is not None:
            display.create_text(
                self.x*dSize[0]//gridSize[0], self.y*dSize[1]//gridSize[1],
                text=t, anchor="nw"
                )

    def getMineNeighbors(self):
        bombs = 0
        for n in self.getNeighbors():
            if n.type == 1:
                bombs += 1
        return bombs

    def getNeighbors(self):
        ns = []
        for x in range(self.x-1, self.x+2):
            for y in range(self.y-1, self.y+2):
                n = self.graph[x, y]
                if n is not None:
                    ns.append(n)
        return ns

    def click(self, e, overwrite=False):
        dSize = [canvas.winfo_width(), canvas.winfo_height()]
        if (self.x*dSize[0]//self.gridSize[0]
                < e.x <
                (self.x+1)*dSize[0]//self.gridSize[0]
                and self.y*dSize[1]//self.gridSize[1]
                < e.y <
                (self.y+1)*dSize[1]//self.gridSize[1]
                or overwrite):
            if self.type == 0:
                self.discovered = True
            else:
                return False
            if self.getMineNeighbors() == 0 and self.type == 0:
                for n in self.getNeighbors():
                    if n.type == 0 and not n.discovered:
                        n.click(e, True)
        return True

    def rightClick(self, e):
        dSize = [canvas.winfo_width(), canvas.winfo_height()]
        if (self.x*dSize[0]//self.gridSize[0]
                < e.x <
                (self.x+1)*dSize[0]//self.gridSize[0]
                and self.y*dSize[1]//self.gridSize[1]
                < e.y <
                (self.y+1)*dSize[1]//self.gridSize[1]):
            self.flag = "F"

    def motion(self, e):
        dSize = [canvas.winfo_width(), canvas.winfo_height()]
        if (self.x*dSize[0]//self.gridSize[0]
                < e.x <
                (self.x+1)*dSize[0]//self.gridSize[0]
                and self.y*dSize[1]//self.gridSize[1]
                < e.y <
                (self.y+1)*dSize[1]//self.gridSize[1]):
            self.mouseHover = True
        else:
            self.mouseHover = False


class Graph:
    def __init__(self, x, y, mines):
        self.x, self.y = x, y
        self.size = (x, y)
        self.graph: typing.List[Cell] = []
        for i in range(playSize[0]):
            self.graph.append([])
            for j in range(playSize[1]):
                self.graph[i].append(
                    Cell(i, j, 1 if random.random()*100 < mines else 0, self))

    def __getitem__(self, item):
        if (item[0] >= self.x or
                item[1] >= self.y or
                item[0] < 0 or
                item[1] < 0):
            return None
        return self.graph[item[0]][item[1]]

    def __iter__(self):
        for i in self.graph:
            for j in i:
                yield j

    def draw(self, display):
        for cell in self:
            cell.draw(display, self.size)

    def click(self, e):
        for cell in self:
            if not cell.click(e):
                return False
        return True

    def rightClick(self, e):
        for cell in self:
            cell.rightClick(e)

    def motion(self, e):
        for cell in self:
            cell.motion(e)
            cell.draw(canvas, (10, 10))


def drawGrid(display: Canvas, width, height):
    w = SIZE[0]//width
    h = SIZE[1]//height
    for i in range(0, SIZE[0], w):
        display.create_line(i, 0, i, SIZE[1], fill=BLACK)

    for i in range(0, SIZE[1], h):
        display.create_line(0, i, SIZE[0], i, fill=BLACK)


graph = Graph(playSize[0], playSize[1], 10)
drawGrid(canvas, 10, 10)
graph.draw(canvas)

# playing = True
# while playing:
#     for u in pg.event.get():
#         if u.type == pg.QUIT:
#             playing = False
#         if u.type == pg.MOUSEBUTTONDOWN:
#             if pg.mouse.get_pressed()[0]:
#                 if not graph.click():
#                     playing = False
#             if pg.mouse.get_pressed()[2]:
#                 graph.rightClick()

#     display.fill(WHITE)
#     graph.draw(display)
#     drawGrid(display, 10, 10)
#     pg.display.update()

display.bind("<Button-1>", graph.click)
display.bind("<Button-3>", graph.rightClick)
display.bind("<Motion>", graph.motion)
display.mainloop()
