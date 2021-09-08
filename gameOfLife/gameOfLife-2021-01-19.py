import math
import logging
from tkinter import Tk, Canvas
import time
import random
DEATH = "death"
ALIVE = "alive"
SEED = 0
auto = False

# logging.basicConfig(level=logging.DEBUG)


class Cell:
    def __init__(self, x, y, state=DEATH):
        self.x, self.y, self.state = x, y, state

    def generation(self, graph):
        alive = 0
        for x in range(self.x-1, self.x+2):
            for y in range(self.y-1, self.y+2):
                if (x, y) != (self.x, self.y):
                    try:
                        if graph[x][y].state == ALIVE:
                            alive += 1
                    except IndexError:
                        pass
        if self.state == ALIVE:
            if alive < 2:
                return Cell(self.x, self.y, DEATH), True
            if alive in [2, 3]:
                return Cell(self.x, self.y, ALIVE), False
            if alive > 3:
                return Cell(self.x, self.y, DEATH), True
        else:
            if alive == 3:
                return Cell(self.x, self.y, ALIVE), True
            else:
                return Cell(self.x, self.y, DEATH), False

    def switchState(self):
        if self.state == ALIVE:
            self.state = DEATH
        else:
            self.state = ALIVE

    def draw(self, canvas, graph):
        width = canvasSize[0]//len(graph)
        height = canvasSize[1]//len(graph[0])
        canvas.create_rectangle(self.x*width, self.y*height, (self.x+1)*width,
                                (self.y+1)*height, fill="#FFF"
                                if self.state == ALIVE else "#333")

    def __repr__(self):
        return self.state[0]


size = (25, 25)
graph = []
for i in range(size[0]):
    graph.append([])
    for j in range(size[1]):
        if math.sin(i) < 0:  # random.random() < SEED:
            state = ALIVE
        else:
            state = DEATH
        graph[i].append(Cell(i, j, state))


def nextGen(graph):
    newGraph = []
    toUpdate = []
    for i, row in enumerate(graph):
        newGraph.append([])
        toUpdate.append([])
        for j, cell in enumerate(graph[i]):
            new = cell.generation(graph)
            newGraph[i].append(new[0])
            toUpdate[i].append(new[1])
    return newGraph, toUpdate


def mouseClick(e):
    width = canvasSize[0]//len(graph)
    height = canvasSize[1]//len(graph[0])
    x = e.x//width
    y = e.y//height
    graph[x][y].switchState()
    graph[x][y].draw(canvas, graph)


window = Tk()
window.title("Game of Life")
canvasSize = (500, 500)
canvas = Canvas(window, width=canvasSize[0],
                height=canvasSize[1], background="#121212")
canvas.pack()


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
            canvas.create_rectangle(i*width, j*height, (i+1)*width, (j+1)
                                    * height, fill="#FFF"
                                    if cell.state == ALIVE else "#333")


drawGraph(canvas, graph)


def doNextGen():
    global graph
    startTime = time.time()
    graph, toUpdate = nextGen(graph)
    logging.debug(f"Next gen took {time.time() - startTime}")
    for i, row in enumerate(toUpdate):
        for j, cell in enumerate(toUpdate[i]):
            graph[i][j].draw(canvas, graph)
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
