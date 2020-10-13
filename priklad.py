from random import randint, choice

def priklad(a,b):
    num0, num1 = randint(a,b), randint(a,b)
    operation = choice(['//','+','*','-'])
    return f"{num0 if num0 >= num1 else num1} {operation} {num1 if num1 < num0 else num0}", ((num0 if num0 >= num1 else num1) + (num1 if num1 <= num0 else num0)) if operation == "+" else ((num0 if num0 >= num1 else num1) - (num1 if num1 <= num0 else num0)) if operation == "-" else ((num0 if num0 >= num1 else num1) * (num1 if num1 <= num0 else num0)) if operation == "*" else  ((num0 if num0 >= num1 else num1) // (num1 if num1 <= num0 else num0)) if operation == "//" else 0

prikladu = range(int(input("Příkladů? ")))
spravne = 0
for _ in prikladu:
    p, v = priklad(0,20)
    if int(input(f"Kolik je {p}? ")) == v:
        print("Správně")
        spravne += 1
    else:
        print("Špatně")

procent = (spravne/len(prikladu))*100
print(f"Máš {procent} % správně. Tvoje znamka je {1 if procent > 80 else 2 if procent > 60 else 3 if procent > 40 else 4 if procent > 20 else 5}")