from engine import *
import random
import json

import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

with open("dungeonText.json", encoding="utf-8") as f:
    graphJson = json.load(f)

for i in graphJson:
    graph.addRoom(**graphJson[i])

# for i in graph.rooms:
#     print(i)

player = Player("A")
#player = Player(input(whiteText("Jak se jmenuješ?\n")))


# for i in graph.rooms:
#     print(i)
#graph.visualize()

playGame(player)