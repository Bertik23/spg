import random

typyPotvor = [["Krysa",3,2,10]
              ["potkan",4,3,15],
              ["veverka",2,4,15],
              ["Vlk",6,4,20],
              ["Bobo",7,7,25],
              ["Tygr",12,13,30],
              ["Lev",13,12,35],
              ["Medvěd",15,11,50],
              ["Drak",20,20,100]]

jmena = ["Albert","Bohouš","Ondřej","Kamila","Vladan","Jirka","Pavel","Daniela","Jakub"]

class Potvora:
    def __init__(self, type, utok, obrana, zivoty):
        self.type = type
        self.name = random.choice(jmena)