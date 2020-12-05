from engine import *
import random
import json


with open("dungeonText.json", encoding="utf-8") as f:
    graphJson = json.load(f)

for i in graphJson:
    graph.addRoom(**graphJson[i])

# for i in graph.rooms:
#     print(i)

player = Player(input(whiteText("Jak se jmenuješ?\n")))


# for i in graph.rooms:
#     print(i)

playGame(player)