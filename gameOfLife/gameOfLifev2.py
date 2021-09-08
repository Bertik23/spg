import math
import logging
from tkinter import Tk, Canvas
from PIL import Image, ImageTk
import time
import random
import json
DEATH = "death"
ALIVE = "alive"
SEED = 0
auto = False
size = (15, 15)


window = Tk()
window.title("Game of Life")
canvasSize = (500, 500)
canvas = Canvas(window, width=canvasSize[0],
                height=canvasSize[1], background="#121212")
canvas.pack()
imSize = (canvasSize[0]//size[0], canvasSize[1]//size[1])
print(imSize)

# logging.basicConfig(level=logging.DEBUG)
tileset = Image.open("gameOfLife/tileset.jpg")
images = {}
with open("gameOfLife/tileset.json") as f:
    tilesetDict = json.load(f)

# for t in tilesetDict:
#     tileset.crop(tilesetDict[t]).show()

for t in tilesetDict:
    images[t] = ImageTk.PhotoImage(
        image=tileset.crop(tilesetDict[t]).resize(imSize)
    )
    print(images[t].height(), images[t].width())

print(images)


class Cell:
    def __init__(self, x, y, state=DEATH):
        self.x, self.y, self.state = x, y, state
        self.image = None

    def getNeighbors(self):
        for x in range(self.x-1, self.x+2):
            for y in range(self.y-1, self.y+2):
                dx = max(0, min(size[0]-1, x))
                dy = max(0, min(size[1]-1, y))
                if (dx, dy) != (self.x, self.y):
                    yield graph[dx][dy]

    def generation(self, graph):
        alive = 0
        for n in self.getNeighbors():
            try:
                if n.state == ALIVE:
                    alive += 1
            except IndexError:
                pass
        if self.state == ALIVE:
            if alive < 2:
                return DEATH
                self.switchState(DEATH)
            if alive in [2, 3]:
                return ALIVE
                self.switchState(ALIVE)
            if alive > 3:
                return DEATH
                self.switchState(DEATH)
        else:
            if alive == 3:
                return ALIVE
                self.switchState(ALIVE)
            else:
                return DEATH
                self.switchState(DEATH)

    def switchState(self, state=None):
        if state is None:
            if self.state == ALIVE:
                self.state = DEATH
            else:
                self.state = ALIVE
        else:
            self.state = state
        self.draw()
        for n in self.getNeighbors():
            n.draw()

    @property
    def imageState(self):
        state = ""
        for d in [[0, -1], [1, 0], [0, 1], [-1, 0]]:
            dx = max(0, min(size[0]-1, self.x+d[0]))
            dy = max(0, min(size[1]-1, self.y+d[1]))
            # print((self.x, self.y), (dx, dy), d)
            n = graph[dx][dy]
            state += "0" if n.state == DEATH else "1"
        return state

    def draw(self):
        width = canvasSize[0]//len(graph)
        height = canvasSize[1]//len(graph[0])
        # canvas.create_rectangle(self.x*width, self.y*height, (self.x+1)*
        # width,
        #                         (self.y+1)*height, fill="#FFF"
        #                         if self.state == ALIVE else "#333")
        t = "0" if self.state == DEATH else self.imageState
        # print(self.imageState)
        if self.image is None:
            self.image = canvas.create_image(
                self.x*width,
                self.y*height,
                image=images[t],
                anchor="nw")
        else:
            canvas.itemconfig(self.image, image=images[t])

    def __repr__(self):
        return self.state[0]


graph = []
for i in range(size[0]):
    graph.append([])
    for j in range(size[1]):
        if math.sin(i) < 0:  # random.random() < SEED:
            state = ALIVE
        else:
            state = DEATH
        # state = DEATH
        graph[i].append(Cell(i, j, state))


def nextGen(graph):
    newStates = []
    for i, row in enumerate(graph):
        newStates.append([])
        for j, cell in enumerate(graph[i]):
            newStates[i].append(cell.generation(graph))
    for i, row in enumerate(graph):
        for j, cell in enumerate(row):
            cell.switchState(newStates[i][j])
    #         newGraph[i].append(new[0])
    #         toUpdate[i].append(new[1])
    # return newGraph, toUpdate


def mouseClick(e):
    # print("--")
    width = canvasSize[0]//len(graph)
    height = canvasSize[1]//len(graph[0])
    x = e.x//width
    y = e.y//height
    graph[x][y].switchState()
    # print(graph[x][y].imageState)
    # graph[x][y].draw()


def drawGrid(canvas: Canvas, graph):
    width = 500//len(graph)
    w = 500  # canvas.winfo_width()
    height = 500//len(graph[0])
    h = 500  # canvas.winfo_height()
    print(width, w, height, h)
    for i in range(0, w, width):
        canvas.create_line([(i, 0), (i, h)], tag='grid_line', fill="#FFF")

    # Creates all horizontal lines at intevals of 100
    for i in range(0, h, height):
        canvas.create_line([(0, i), (w, i)], tag='grid_line', fill="#FFF")


drawGrid(canvas, graph)


def drawGraph(canvas: Canvas, graph):
    width = canvasSize[0]//len(graph)
    height = canvasSize[1]//len(graph[0])
    for i, row in enumerate(graph):
        for j, cell in enumerate(graph[i]):
            cell.draw()
            # canvas.create_rectangle(i*width, j*height, (i+1)*width, (j+1)
            #                         * height, fill="#FFF"
            #                         if cell.state == ALIVE else "#333")


drawGraph(canvas, graph)


def doNextGen():
    global graph
    startTime = time.time()
    # graph, toUpdate = nextGen(graph)
    nextGen(graph)
    logging.debug(f"Next gen took {time.time() - startTime}")
    # for i, row in enumerate(toUpdate):
    #     for j, cell in enumerate(toUpdate[i]):
    #         graph[i][j].draw(canvas, graph)
    logging.debug(f"Drawing took {time.time() - startTime}")
    if auto:
        logging.debug("Going auto mode")
        canvas.update_idletasks
        window.after(200, doNextGen)


def spacePress(e):
    doNextGen()


def enter(e):
    global auto
    if auto:
        auto = False
    else:
        auto = True
    print(auto)


window.bind("<Button-1>", mouseClick)
window.bind("<KeyPress-space>", spacePress)
window.bind("<KeyPress-Return>", enter)


window.mainloop()
