from tkinter import Tk, Canvas
import random

POCET = 40
VEL = 800/POCET
FPS = 30
DROBKY = 10

randomColor = lambda: "#%06x" % random.randint(0, 0xFFFFFF)

class Bunka:
    def __init__(self, x,y):
        self.vzhled = platno.create_rectangle(x*VEL, y*VEL+50, (x+1)*VEL, (y+1)*VEL+50, fill="white",outline="white")
        self.x, self.y = x,y
        self.cislo = 0
        self.text = platno.create_text(x*VEL+VEL/2, y*VEL+VEL/2+50, text=(self.x,self.y), anchor="center")

class Had:
    def __init__(self, x, y, delka, smer, barva, jmeno="Anonym", hrac=False, **kwargs):
        self.x, self.y, self.delka, self.smer, self.barva, self.jmeno, self.hrac = x, y, delka, smer, barva, jmeno, hrac
        if hrac:
            self.nahoru = kwargs.pop("nahoru")
            self.dolu = kwargs.pop("dolu")
            self.doleva = kwargs.pop("doleva")
            self.doprava = kwargs.pop("doprava")
    def logika(self):
        def getSmer(x,y, node):
            if x == node[0]:
                if y == 0 and node[1] == POCET-1:
                    return 1
                elif y == POCET-1 and node[1] == 0:
                    return 3
                elif y > node[1]:
                    return 1
                elif y < node[1]:
                    return 3
            if y == node[1]:
                if x == 0 and node[0] == POCET-1:
                    return 4
                elif x == POCET-1 and node[0] == 0:
                    return 2
                elif x > node[0]:
                    return 4
                elif x < node[0]:
                    return 2

        queue = [(self.x,self.y, 0, False, ())]
        values = []
        end = None
        for i in range(POCET):
            values.append([])
            for j in range(POCET):
                values[i].append(float("inf"))
        a = 0
        for q in queue:
            a += 1
            #print(q, a)
            if q[2] >= POCET*2:
                if q[3] and q[4] != ():
                    end = q[4]
                break
            if sit[q[0]][q[1]].cislo == -1:
                if q[3]:
                    end = q
                    break
                else:
                    q = (*q[:3], True, q)
            for x in range(q[0]-1, q[0]+2):
                for y in range(q[1]-1, q[1]+2):
                    x = x%POCET
                    y = y%POCET
                    if (x,y) == (q[0], q[1]) or (x != q[0] and y != q[1]):
                        continue
                    if sit[x][y].cislo <= 0 and values[x][y] > q[2]+1:
                        #print(x,y, values[x][y], sit[x][y].cislo)
                        # if sit[x][y].cislo == -1:
                        #     print("Drobek")
                        values[x][y] = q[2]+1
                        #platno.itemconfig(sit[x][y].text, text=str(q[2]+1))
                        queue.append((x,y, q[2]+1, q[3], q[4]))
        # print("pathFound")
        # print(end)
        for i,row in enumerate(sit):
            for j,cell in enumerate(row):
                platno.itemconfig(cell.text, text=values[i][j])

        if end != None:
            path = []
            node = end
            found = False
            smer = None
            while not found:
                path.append(node)
                b = False
                for x in range(node[0]-1, node[0]+2):
                    for y in range(node[1]-1, node[1]+2):
                        x = x%POCET
                        y = y%POCET
                        if (x,y) == (node[0], node[1]) or (x != node[0] and y != node[1]):
                            continue
                        if (x,y) == (self.x, self.y):
                            smer = getSmer(x,y,node)
                            #print((self.x, self.y),(x,y),node, smer)
                            found = True
                        if values[x][y] < node[2]:
                            node = (x,y,values[x][y])
                            b = True
                            break
                    if b:
                        break
            pathCoords = []
            for p in path:
                pathCoords.extend([p[0]*VEL+VEL/2, p[1]*VEL+VEL/2+50])
            if len(pathCoords) > 2:
                if getattr(self, "line", None) == None:
                    self.line = platno.create_line(*pathCoords, fill=self.barva)
                else:
                    platno.coords(self.line, *pathCoords)
            self.smer = smer
        else:
            volnost = [0,0,0,0]
            for x in range(self.x+1, self.x+1+POCET):
                x = x%POCET
                #print(x, self.y ,sit[x][self.y].cislo)
                if sit[x][self.y].cislo == 0:
                    volnost[1] += 1
                else:
                    break
            for x in range(self.x-1,self.x-POCET, -1):
                x = x%POCET
                #print(x, self.y, sit[x][self.y].cislo)
                if sit[x][self.y].cislo == 0:
                    volnost[3] += 1
                else:
                    break
            for y in range(self.y+1, self.y+1+POCET):
                y = y%POCET
                #print(self.x, y, sit[self.x][y].cislo)
                if sit[self.x][y].cislo == 0:
                    volnost[2] += 1
                else:
                    break
            for y in range(self.y-1, self.y-POCET, -1):
                y = y%POCET
                #print(self.x, y, sit[self.x][y].cislo)
                if sit[self.x][y].cislo == 0:
                    volnost[0] += 1
                else:
                    break
            smer = max(range(len(volnost)), key=volnost.__getitem__)+1
            #print(volnost, smer)
            self.smer = smer
        x,y = self.x, self.y
        if self.smer == 1:
            y -= 1
        if self.smer == 2:
            x += 1
        if self.smer == 3:
            y += 1
        if self.smer == 4:
            x -= 1
        x = x%POCET
        y = y%POCET
        if sit[x][y].cislo > 0:
            print("Smrt")
            platno.delete(getattr(self,"line",None))


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
                #platno.itemconfig(j.text, text=str(j.cislo))
                if j.cislo == 0:
                    platno.itemconfig(j.vzhled, fill="white")
    #okno.after(1000//FPS, pohyb)

def drobek():
    x,y = random.randint(0,POCET-1),random.randint(0,POCET-1)
    while sit[x][y].cislo != 0:
        x,y = random.randint(0,POCET-1),random.randint(0,POCET-1)
    sit[x][y].cislo = -1
    platno.itemconfig(sit[x][y].vzhled, fill="#FF00FF")

okno = Tk()
okno.title("Snake")
platno = Canvas(okno, height = 850, width = 800)
platno.pack()

sit = []

for i in range(POCET):
    sit.append([Bunka(i,j) for j in range(POCET)])

barvy = ["#5442f5","#f54242","#4ef542","#00a383","#a9b52a","#000000","#7f00ba","#ba6900","#ff0000","#499100"]

# hadi = [Had(5,5, delka=5, smer = 1, barva="#FF0000", jmeno="Bobík", hrac=False, nahoru="Up", doprava="Right", dolu = "Down", doleva="Left"),
#         Had(9,9, delka=20, smer = 2, barva="#00FF00", jmeno="Adík", hrac=False, nahoru="w", doprava="d", dolu = "s", doleva="a")]

hadi = [Had(random.randint(0,POCET-1), random.randint(0,POCET-1), delka=5, smer=random.randint(0,4), barva=barvy[i], jmeno="", hrac=False) for i in range(1)]

for i in range(DROBKY):
    drobek()

okno.bind("<Key>", stisk)
okno.bind("<KeyPress-space>", lambda x: pohyb())
#pohyb()

okno.mainloop()