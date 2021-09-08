from tkinter import Tk, Canvas
from random import randint


class Bunka:
    def __init__(self, x, y):
        self.vzhled = platno.create_rectangle(x*VEL, y*VEL+50, (x+1)*VEL,
                                              (y+1)*VEL + 50, fill="white",
                                              width=0)
        self.cislo = 0


class Had:
    def __init__(self, x, y, delka, smer, barva, jmeno="Anonym", hrac=False,
                 nahoru="", doprava="", dolu="", doleva=""):
        self.x = x
        self.y = y
        self.delka = delka
        self.smer = smer
        self.barva = barva
        self.jmeno = jmeno
        self.hrac = hrac
        self.nahoru = nahoru
        self.dolu = dolu
        self.doprava = doprava
        self.doleva = doleva

    def logika(self):
        """Funkce, která mění self.smer"""
        def getSmer(x, y, node):
            """Funkce, která vrátí směr ve kterém se nachází buňka
            `node` vzhledem k buňce `(x,y)`
            Funguje pouze pro sousedící buňky"""
            # Jestli v jedné rovině
            if x == node[0]:
                if y == 0 and node[1] == POCET-1:
                    return 1
                elif y == POCET-1 and node[1] == 0:
                    return 3
                elif y > node[1]:
                    return 1
                elif y < node[1]:
                    return 3
            # Jestli jsou nad sebou
            if y == node[1]:
                if x == 0 and node[0] == POCET-1:
                    return 4
                elif x == POCET-1 and node[0] == 0:
                    return 2
                elif x > node[0]:
                    return 4
                elif x < node[0]:
                    return 2

        def pathFind(start, r=0):
            """Funkce, která najde,
            jestli je cesta z buňky `start` k drobku."""
            queue = [(start[0], start[1], 0)]  # Udělá queue, se startem,
            # kterému přiřadí hodnotu 0
            # Vytvoření matice pro ukládání hodnod buněk
            values = []
            for i in range(POCET):
                values.append([])
                for j in range(POCET):
                    values[i].append(float("inf"))
            end = None  # Konec je None
            # Pokud je zavolána z rekurze vrať None
            if r >= 2:
                return None, values

            # Procházení queue
            for q in queue:
                # Pokud je q drobek a neni start
                if (sit[q[0]][q[1]].cislo == -1 and
                        q[:2] != (start[0], start[1])):
                    newEnd = pathFind(q[:2], r=r+1)[0]  # Najdi jesli je z
                    # drobku cesta do dalšího drobku, vyřadí slepé uličky
                    end = q  # Konec je drobek
                    # Pokud je cesta do dalšího drobku nebo bylo zavoláno z
                    # rekurze
                    if (newEnd is not None and r == 0) or (r > 0):
                        return end, values
                # Procházení sousedů q
                for x in range(q[0]-1, q[0]+2):
                    for y in range(q[1]-1, q[1]+2):
                        # Přechod přes hrany do +
                        x = x % POCET
                        y = y % POCET
                        # Vyřazení q a sousedů sousedících vrcholem
                        if (x, y) == (q[0], q[1]) or (x != q[0] and y != q[1]):
                            continue
                        # Pokud soused není kus hada a jeho hodnota je větší
                        # než hodnota q
                        if sit[x][y].cislo <= 0 and values[x][y] > q[2]+1:
                            values[x][y] = q[2]+1  # Nastav novou hodnotu
                            queue.append((x, y, q[2]+1))  # Přidej souseda
                            # do queue
            # Pokud nebyl nebyl nalezen žádný drobek, nebo jen jeden
            return end, values
        end, values = pathFind((self.x, self.y))

        # Pokud byl nalezen drobek
        if end is not None:
            path = []
            node = end  # Nastavení aktuální pozice na konec
            found = False  # Jestli byla nalezena cesta
            smer = None
            # Dokud nebyla nalezena cesta
            while not found:
                # Do cesty přidej aktuální pozici
                path.append(node)
                b = False
                # Procházení sousedů
                for x in range(node[0]-1, node[0]+2):
                    for y in range(node[1]-1, node[1]+2):
                        # Přecházení přes okraje
                        x = x % POCET
                        y = y % POCET
                        # Vyřazení aktuální pozice a sousedů sousedících
                        # vrcholem
                        if ((x, y) == (node[0], node[1]) or
                                (x != node[0] and y != node[1])):
                            continue
                        # Pokud je soused hlava hada
                        if (x, y) == (self.x, self.y):
                            smer = getSmer(x, y, node)  # Najdi směr kam jít
                            found = True  # Cesta byla nalezena
                        # Pokud má soused nižší hodnotu než aktuální pozice
                        if values[x][y] < node[2]:
                            # Nastav souseda na aktuální pozici
                            node = (x, y, values[x][y])
                            b = True  # Pokračování s novou aktuální pozicí
                            break
                    if b:
                        break
            # Kreslení cesty
            pathCoords = []
            # Procházení cestou
            for p in path:
                # Přidá souřadnice do seznamu
                pathCoords.extend([p[0]*VEL+VEL/2, p[1]*VEL+VEL/2+50])
            # Pokud má cesta více než 1 bod
            if len(pathCoords) > 2:
                # Pokud neexistuje nákres cesty
                if getattr(self, "line", None) is None:
                    self.line = platno.create_line(
                        *pathCoords, fill=self.barva)  # Vytvoř nákres cesty
                else:
                    platno.coords(self.line, *pathCoords)  # Uprav nákres cesty
            self.smer = smer  # Nastav self.smer na nalezený směr
        # Pokud nebyl nalezen drobek
        else:
            # Hledání směru, kde je nejvíc místa
            volnost = [0, 0, 0, 0]
            for x in range(self.x+1, self.x+1+POCET):
                x = x % POCET
                if sit[x][self.y].cislo == 0:
                    volnost[1] += 1
                else:
                    break
            for x in range(self.x-1, self.x-POCET, -1):
                x = x % POCET
                if sit[x][self.y].cislo == 0:
                    volnost[3] += 1
                else:
                    break
            for y in range(self.y+1, self.y+1+POCET):
                y = y % POCET
                if sit[self.x][y].cislo == 0:
                    volnost[2] += 1
                else:
                    break
            for y in range(self.y-1, self.y-POCET, -1):
                y = y % POCET
                if sit[self.x][y].cislo == 0:
                    volnost[0] += 1
                else:
                    break
            # Nalezení směru s nejvíc místem
            smer = max(range(len(volnost)), key=volnost.__getitem__)+1
            self.smer = smer

    def __del__(self):
        # Smazání nákresu cesty
        platno.delete(getattr(self, "line", None))


def pohyb():
    for had in hadi:
        # Volání počítačem ovládaných hadů
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
        if had.x < 0:
            had.x = POCET-1
        if had.y < 0:
            had.y = POCET-1
        if had.x == POCET:
            had.x = 0
        if had.y == POCET:
            had.y = 0

        if sit[had.x][had.y].cislo > 0:
            hadi.remove(had)
            continue
        if sit[had.x][had.y].cislo == -1:
            had.delka += 1
            drobek()
        sit[had.x][had.y].cislo = had.delka + 1

        platno.itemconfig(sit[had.x][had.y].vzhled, fill=had.barva)

    for i in range(POCET):
        for j in range(POCET):
            if sit[i][j].cislo > 0:
                sit[i][j].cislo -= 1
                # platno.itemconfig(sit[i][j].text, text = sit[i][j].cislo)
                if sit[i][j].cislo == 0:
                    platno.itemconfig(sit[i][j].vzhled, fill="white")

    okno.after(1000//FPS, pohyb)


def drobek():
    x = randint(0, POCET-1)
    y = randint(0, POCET-1)
    while sit[x][y].cislo != 0:
        x = randint(0, POCET-1)
        y = randint(0, POCET-1)
    sit[x][y].cislo = -1
    platno.itemconfig(sit[x][y].vzhled, fill="orange")


def stisk(e):
    k = e.keysym
    for had in hadi:
        if had.hrac:
            if k == had.nahoru and had.smer != 3:
                had.smer = 1
            if k == had.doprava and had.smer != 4:
                had.smer = 2
            if k == had.dolu and had.smer != 1:
                had.smer = 3
            if k == had.doleva and had.smer != 2:
                had.smer = 4


POCET = 40
VEL = 500/POCET
FPS = 20
DROBKY = 10
okno = Tk()
platno = Canvas(okno, height=550, width=500)
platno.pack()

sit = []

for i in range(POCET):
    sit.append([])
    for j in range(POCET):
        sit[i].append(Bunka(i, j))

hadi = [
    Had(x=10, y=10, delka=1, smer=1, barva="red", jmeno="Jarda", hrac=False,
        nahoru="Up", doprava="Right", dolu="Down", doleva="Left"),
    Had(x=5, y=5, delka=20, smer=3, barva="blue", jmeno="Pepa", hrac=False,
        nahoru="w", doprava="d", dolu="s", doleva="a"),
    Had(x=20, y=20, delka=1, smer=1, barva="black", jmeno="Komp", hrac=False)
]
for i in range(DROBKY):
    drobek()
okno.bind("<Key>", stisk)
pohyb()
okno.mainloop()
