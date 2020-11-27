import random

with open("2020-11-24/encs.txt", encoding="utf-8") as f:
    slovnik = [i.split("|") for i in f.read().split("\n")[:-1]]

def listToString(l, withIndex=False):
    out = ""
    for index, i in enumerate(l):
        out += f"{f'{index+1}) ' if withIndex else ''}{i}, "
    return out[:-2]

pocetMoznosti = 5
spravne = 0
otazek = 0
while True:
    volba = random.choice(slovnik)
    aj = volba[0]
    cj = volba[1]
    wrong = [random.choice(slovnik)[1] for i in range(pocetMoznosti-1)]
    moznosti = wrong.copy()
    moznosti.insert(random.randint(0,pocetMoznosti), cj)
    #print(aj,cj, moznosti, wrong)
    i = input(f"Přelož: {aj} do češtiny.\nMožnosti: {listToString(moznosti, True)}\n")
    try:
        intI = int(i)-1
    except:
        intI = -1
    if i == cj:
        spravne += 1
        print("Správně!\n----------")
    elif moznosti[intI] == cj and intI != -1:
        spravne += 1
        print("Správně!\n----------")
    else:
        print(f"Špatně, správně bylo {cj}\n----------")
    otazek += 1