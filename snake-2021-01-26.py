from tkinter import Tk, Canvas
import random

POCET = 40
VEL = 500/POCET
FPS = 20
DROBKY = 10

class Bunka:
    def __init__(self, x,y):
        self.vzhled = platno.create_rectangle(x*VEL, y*VEL+50, (x+1)*VEL, (y+1)*VEL+50, fill="white")
        self.x, self.y = x,y
        self.cislo = 0
        self.text = platno.create_text(x*VEL+VEL/2, y*VEL+VEL/2+50, text=self.cislo, anchor="center")

class Had:
    def __init__(self, x, y, delka, smer, barva, jmeno="Anonym", hrac=False, **kwargs):
        self.x, self.y, self.delka, self.smer, self.barva, self.jmeno, self.hrac = x, y, delka, smer, barva, jmeno, hrac
        if hrac:
            self.nahoru = kwargs.pop("nahoru")
            self.dolu = kwargs.pop("dolu")
            self.doleva = kwargs.pop("doleva")
            self.doprava = kwargs.pop("doprava")
    def logika(self):
        queue = [(self.x,self.y, 0)]
        values = []
        end = None
        for i in range(POCET):
            values.append([])
            for j in range(POCET):
                values[i].append(float("inf"))
        for q in queue:
            if sit[q[0]][q[1]] == -1:
                end = q
                break
            for x in range(q[0]-1, q[0]+2):
                for y in range(q[1]-1, q[1]+2):
                    if sit[x][y] <= 0 and  values[x][y] > q[2]+1:
                        queue.append((x,y, q[2]+1))
        node = end
        while True:
            b = False
            for x in range(node[0]-1, node[0]+2):
                for y in range(node[1]-1, node[1]+2):
                    if values[x][y] < node[2]:
                        node = (x,y,values[x,y])
                        b = True
                        break
                if b:
                    break


def stisk(e):
    k = e.keysym
    for had in hadi:
        if had.hrac:
            if k == had.nahoru and had.smer != 3:
                had.smer = 1
            if k == had.doleva and had.smer != 2:
                had.smer = 4
            if k == had.dolu and had.smer != 1:
                had.smer = 3
            if k == had.doprava and had.smer != 4:
                had.smer = 2

def pohyb():
    for had in hadi:
        #pc controled had
        if not had.hrac:
            had.logika()
        if had.smer == 1:
            had.y -= 1
        if had.smer == 2:
            had.x += 1
        if had.smer == 3:
            had.y += 1
        if had.smer == 4:
            had.x -= 1
        had.x = had.x%POCET
        had.y = had.y%POCET
        if sit[had.x][had.y].cislo > 0:
            hadi.remove(had)
            continue
        elif sit[had.x][had.y].cislo == -1:
            had.delka += 1
            drobek()
        sit[had.x][had.y].cislo = had.delka

        platno.itemconfig(sit[had.x][had.y].vzhled, fill=had.barva)


    for i in sit:
        for j in i:
            if j.cislo > 0:
                j.cislo -= 1
                platno.itemconfig(j.text, text=str(j.cislo))
                if j.cislo == 0:
                    platno.itemconfig(j.vzhled, fill="white")
    okno.after(1000//FPS, pohyb)

def drobek():
    x,y = random.randint(0,POCET-1),random.randint(0,POCET-1)
    while sit[x][y].cislo != 0:
        x,y = random.randint(0,POCET-1),random.randint(0,POCET-1)
    sit[x][y].cislo = -1
    platno.itemconfig(sit[x][y].vzhled, fill="#FF00FF")

okno = Tk()
okno.title("Snake")
platno = Canvas(okno, height = 550, width = 500)
platno.pack()

sit = []

for i in range(POCET):
    sit.append([Bunka(i,j) for j in range(POCET)])

hadi = [Had(5,5, delka=5, smer = 1, barva="#FF0000", jmeno="Bobík", hrac=False, nahoru="Up", doprava="Right", dolu = "Down", doleva="Left")]#,
        #Had(9,9, delka=20, smer = 2, barva="#00FF00", jmeno="Adík", hrac=True, nahoru="w", doprava="d", dolu = "s", doleva="a")]

for i in range(DROBKY):
    drobek()

okno.bind("<Key>", stisk)
pohyb()

okno.mainloop()