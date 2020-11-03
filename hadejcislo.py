from random import randint

print("Myslím si číslo mezi 0 a 100")
number = randint(0,100)
pokus = 0
while True:
    try:
        guess = int(input("Jaké číslo si myslím? "))
        pokus += 1
    except:
        print("Číslo!")
        continue
    if guess > number: print("Zmenši")
    elif guess < number: print("Zvětši")
    elif guess == number:
        print(f"Správně uhodl jsi na {pokus}. pokus")
        break