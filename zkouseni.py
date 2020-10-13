#Zkoušení z matematiky
from random import randint


def priklad():
    typ = randint(0,3)
    if typ == 0:
        #Sčítání
        a = randint(1,20)
        b = randint(1,20)
        zadani = str(a) + " + " + str(b)
        spravne = a + b
    elif typ == 1:
        #Odčítání
        spravne = randint(0,20)
        b = randint(0,20)
        a = spravne + b
        zadani = str(a) + " - " + str(b)
    elif typ == 2:
        #Násobení
        a = randint(1,20)
        b = randint(1,20)
        spravne = a*b
        zadani = f"{a} * {b}"
    else:
        #Dělení
        spravne = randint(0,20)
        b = randint(0,20)
        a = spravne * b
        zadani = f"{a} / {b}"
        
    return zadani, spravne

kolik = int(input("Kolik chceš příkladů:"))

score = 0
for i in range(1,kolik+1):
    print("Příklad "+str(i)+":")
    zadani, spravne = priklad()
    odpoved =int(input(zadani+" = "))
    if odpoved == spravne:
        print("Správně")
        score += 1
    else:
        print("Špatně, správně je " + str(spravne))

procent = (score/kolik)*100
print(f"Máš {procent} % správně. Tvoje znamka je {1 if procent > 80 else 2 if procent > 60 else 3 if procent > 40 else 4 if procent > 20 else 5}")

#Známky:
#<20% chyb 1
#<40% 2
#<60% 3
#<80% 4
# 5