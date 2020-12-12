import random

sirky = random.randint(5,30)
#sirky = 5

def pocitac():
    global sirky, varianta
    print("Hraje počítač.")
    if varianta.lower() == "a":
        odeber = (sirky-1)%4
    else:
        odeber = sirky%4
    if odeber == 0:
        odeber = random.randint(1,min(sirky,3))
    print(f"Počítač odebírá {odeber} sirek")
    sirky -= odeber

def hrac():
    global sirky
    odeber = -1
    while odeber < 1 or odeber > min(sirky,3):
        odeber = input("Kolik sirek chceš odebrat?\n")
        try:
            odeber = int(odeber)
        except ValueError:
            odeber = -1
    sirky -= odeber

def vypis():
    global sirky
    print(f"Na slole leží {sirky} sirek")

tah = 0
varianta = "C"
while varianta.lower() not in ("a","b"):
    varianta = input("Jakou variantu chceš?\nA - prohrává ten, co bere poslední\nB - vyhrává ten, co bere poslední\n")

while sirky > 0:
    vypis()
    if tah%2 == 0:
        hrac()
    else:
        pocitac()
    tah += 1

if varianta.lower() == "a":
    print(["Vyhrál jsi.", "Prohrál jsi"][tah%2])
else:
    print(["Prohrál jsi","Vyhrál jsi"][tah%2])
