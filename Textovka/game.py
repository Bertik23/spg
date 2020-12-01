from engine import *
import random

for i in [0,1,2,3,4,5]:
    graph.addRoom(i, f"Místnost {i+1}", "Popis", [random.choice([0,1,2,3,4,5,6]) for _ in range(2)])

for i in graph.rooms:
    print(i)

player = Player(input("Jak se jmenuješ?\n"))


graph.addRoom(10, "Test", "Test", [0,1])
for i in graph.rooms:
    print(i)

playGame(player)