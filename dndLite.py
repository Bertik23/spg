import random
import time

creatureTypes = [["Krysa",3,2,10],
              ["potkan",4,3,15],
              ["veverka",2,4,15],
              ["Vlk",6,4,20],
              ["Bobo",7,7,25],
              ["Tygr",12,13,30],
              ["Lev",13,12,35],
              ["Medvěd",15,11,50],
              ["Drak",20,20,100]]

names = ["Albert","Bohouš","Ondřej","Kamila","Vladan","Jirka","Pavel","Daniela","Jakub"]

class Creature:
    def __init__(self, typ: int):
        self.typ = typ
        self.typeName = creatureTypes[typ][0]
        self.name = random.choice(names)
        self.attack = creatureTypes[typ][1]
        self.defense = creatureTypes[typ][1]
        self.lives = creatureTypes[typ][1]
        self.expDrop = (self.attack + self.defense)*6 + self.lives

    def __str__(self):
        return f"{self.typeName} {self.name}, attack: {self.attack}, defense: {self.defense}, lives: {self.lives}"

class Hero:
    def __init__(self):
        self.level = 1
        self.exp = 0
        self.attack = 7
        self.defense = 7
        self.lives = 20
        self.maxLives = 20
        self.nextLevel = 100
        self.death = False

    def attackCreature(self, creature: Creature):
        while self.lives > 0 and creature.lives > 0:
            u = self.attack + random.randint(-9,9) - creature.defense
            if u > 0:
                creature.lives -= u
                print(f"Ubral jsi {u} životů")
            else:
                print("Minul jsi")
            if creature.lives <= 0:
                return
            u = creature.attack + random.randint(-9,9) - self.defense
            if u > 0:
                self.lives -= u
                print(f"Přišel jsi o {u} životů")
            else:
                print("Vedle")
            if self.lives <= 0:
                return
            print(self)
            print(creature)

    def addExp(self, exp):
        self.exp += exp
        while self.exp >= self.nextLevel:
            self.level += 1
            self.attack += random.randint(1,6)
            self.maxLives += random.randint(1,6)
            self.defense += random.randint(1,6)
            self.exp -= self.nextLevel
            self.nextLevel += round(self.nextLevel*1.5)
            print(f"Level up ({self.level})")

    
    def __str__(self):
        return f"Ty, level: {self.level}, attack: {self.attack}, defense: {self.defense}, lives: {self.lives}"

class World:
    def __init__(self, numOfCretures: int):
        self.creatures = []
        for i in range(numOfCretures):
            self.creatures.append(Creature(random.randint(0,len(creatureTypes)-1)))
        self.hero = Hero()
        self.game()
    def game(self):
        while len(self.creatures) > 0 and not self.hero.death:
            for i, creature in enumerate(self.creatures):
                print(f"{i}: {creature}")
            print("-"*20)
            print(self.hero)
            print("-"*20)
            attack = input("Number of attacked creature: ")
            while not attack.isdigit():
                attack = input("Number of attacked creature: ")
            self.hero.attackCreature(self.creatures[int(attack)])
            if self.creatures[int(attack)].lives <= 0:
                self.hero.addExp(self.creatures[int(attack)].expDrop)
                self.creatures.pop(int(attack))
            if self.hero.lives <= 0:
                self.hero.death = 0
            time.sleep(1)

w = World(20)