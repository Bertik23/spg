import math
import logging
from tkinter import Tk, Canvas
import time
import random
import json


BLACK = "black"
WHITE = "white"
SEED = 0
auto = False

# logging.basicConfig(level=logging.DEBUG)


class Cell:
    def __init__(self, x, y, state=BLACK):
        self.x, self.y, self.state = x, y, state

    def switchState(self):
        if self.state == WHITE:
            self.state = BLACK
        else:
            self.state = WHITE

    def draw(self, canvas, graph):
        width = canvasSize[0]//len(graph)
        height = canvasSize[1]//len(graph[0])
        canvas.create_rectangle(self.x*width, self.y*height, (self.x+1)*width,
                                (self.y+1)*height, fill="#FFF"
                                if self.state == WHITE else "#333")

    def __repr__(self):
        return self.state[0]

    def save(self):
        return self.state[0]


size = (25, 25)
graph = []
for i in range(size[0]):
    graph.append([])
    for j in range(size[1]):
        state = BLACK
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
window.title("Animator 3000")
canvasSize = (500, 500)
canvas = Canvas(window, width=canvasSize[0],
                height=canvasSize[1], background="#121212")
canvas.pack()


anim = {}


def strGraph():
    out = ""
    for row in graph:
        for c in row:
            out += c.save()
        out += "\n"
    out = out[:-1]
    return out


def addToAnim():
    anim[str(len(anim))] = strGraph()
    print(f"Step {len(anim)} added.")


def saveAnimation():
    with open("animation.anim", "w") as f:
        json.dump(anim, f)
    print("Animation saved!")


def loadAnimation():
    global anim
    with open("animation.anim", "r") as f:
        anim = json.load(f)
    print("Animation loaded!")


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
                                    if cell.state == WHITE else "#333")


def runAnimation(step):
    if str(step) in anim.keys():
        print(f"Running step {step}")
        for i, row in enumerate(anim[str(step)].split("\n")):
            for ii, c in enumerate(row):
                graph[i][ii].state = BLACK if c == "b" else WHITE
                graph[i][ii].draw(canvas, graph)
        window.after(500, runAnimation, step+1)
    else:
        print("Not Running")


drawGraph(canvas, graph)


def spacePress(e):
    runAnimation(0)


def enter(e):
    saveAnimation()


def l(e):
    loadAnimation()


def nextStep(e):
    addToAnim()


window.bind("<Button-1>", mouseClick)
window.bind("<KeyPress-space>", spacePress)
window.bind("<KeyPress-s>", nextStep)
window.bind("<KeyPress-Return>", enter)
window.bind("<KeyPress-l>", l)

print(
    """
    Vítej v Animátoru 3000

    Návod:
    - L: Načte animaci ze souboru "animation.anim".
    - S: Přidá aktuální obraz na konec animace.
    - Enter: Uloží animaci do "animation.anim"
    - Space: Přehraje načtenou animaci.
    """
)

window.mainloop()
