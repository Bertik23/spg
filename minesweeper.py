from tkinter import Tk, Canvas
from random import randint, random
from PIL import ImageTk, Image

POCET = 20
# POCET_MIN = 10
VELIKOST = int(500/POCET)
OBTIZNOST = 0.01
BARVY = [
    "#000",
    "blue",
    "green",
    "red",
    "#007",
    "brown",
    "#A4A",
    "yellow",
    "black"
]

flaged = 0
mines = 0


class Cell:
    def __init__(self, x, y, m):
        global mines
        self.x = x
        self.y = y
        self.color = "#0F0"
        self.covered = True
        self.mina = True if random() <= OBTIZNOST else False
        self.flagImg = None
        if self.mina:
            mines += 1
            # print("1", self.mina)
            canvas.create_image(
                x*VELIKOST,
                y*VELIKOST,
                image=minaImg,
                anchor="nw"
            )
        else:
            self.vzhled = canvas.create_rectangle(
                x*VELIKOST,
                y*VELIKOST,
                (x+1)*VELIKOST,
                (y+1)*VELIKOST,
                outline=self.color
                )

    def precisluj(self, n):
        self.cislo = n
        if n != 0 and not self.mina:
            # print(self.mina)
            self.cisloText = canvas.create_text(self.x*VELIKOST + VELIKOST/2,
                                                self.y*VELIKOST + VELIKOST/2,
                                                text=str(n), font=(
                                                    "Roboto",
                                                    VELIKOST//2),
                                                fill=BARVY[n])
        if self.covered:
            self.cover = canvas.create_image(
                self.x*VELIKOST,
                self.y*VELIKOST,
                image=coverImg,
                anchor="nw"
                )

    def uncover(self, end=False):
        if not self.covered or (self.flagImg is not None and not end):
            return
        self.covered = False
        canvas.delete(self.cover)
        if self.cislo == 0 and not end:
            toUncover = [[False for i in range(POCET)] for j in range(POCET)]
            queue = [(self.x, self.y)]
            for q in queue:
                for x in range(max(0, q[0]-1), min(POCET, q[0]+2)):
                    for y in range(max(0, q[1]-1), min(POCET, q[1]+2)):
                        if not toUncover[x][y] and pole[x][y].cislo == 0:
                            queue.append((x, y))
                        toUncover[x][y] = True
            for x, r in enumerate(toUncover):
                for y, cell in enumerate(r):
                    if cell:
                        pole[x][y].uncover(True)
        if self.mina and not end:
            end(False)

    def flag(self):
        global mines, flaged
        if self.flagImg is None:
            self.flagImg = canvas.create_image(
                self.x*VELIKOST,
                self.y*VELIKOST,
                image=flagImg,
                anchor="nw"
            )
            if self.mina:
                flaged += 1
                if flaged == mines:
                    end(True)
        else:
            canvas.delete(self.flagImg)
            self.flagImg = None
            if self.mina:
                flaged -= 1


def start():
    # pole = [[Cell(x, y, False) for x in range(POCET)] for y in range(POCET)]
    for y in range(POCET):
        for x in range(POCET):
            n = 0
            for nx in range(-1, 2):
                for ny in range(-1, 2):
                    # and (nx!=0 and ny!=0):
                    if 0 <= x + nx < POCET and 0 <= y + ny < POCET:
                        if pole[x + nx][y + ny].mina:
                            n += 1
            pole[x][y].precisluj(n)


def end(win):
    if win:
        print("WIN!")
        canvas.create_text(10, 510, text="Vyhrál jsi!", anchor="nw")
    else:
        for row in pole:
            for cell in row:
                cell.uncover(True)


def click(e):
    i, j = int(e.x/VELIKOST), int(e.y/VELIKOST)
    if i > POCET or j > POCET:
        return
    pole[i][j].uncover()


def rightClick(e):
    i, j = int(e.x/VELIKOST), int(e.y/VELIKOST)
    if i > POCET or j > POCET:
        return
    pole[i][j].flag()


window = Tk()
window.title("Minesweeper")
canvas = Canvas(window, height=600, width=500)
canvas.pack()
# pozadi = ImageTk.PhotoImage(file = "pozadi.jpg")
# platno.create_image(250,250,image=pozadi)
minaImg = ImageTk.PhotoImage(image=Image.open(
    "images\\mina.png").resize((VELIKOST, VELIKOST), True))
coverImg = ImageTk.PhotoImage(image=Image.open(
    "images\\button.png").resize((VELIKOST, VELIKOST), True))
flagImg = ImageTk.PhotoImage(image=Image.open(
    "images\\flag.png").resize((VELIKOST, VELIKOST), True))
pole = [[Cell(x, y, False) for y in range(POCET)] for x in range(POCET)]

start()

window.bind("<Button-1>", click)
window.bind("<Button-3>", rightClick)
window.mainloop()
