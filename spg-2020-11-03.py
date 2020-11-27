import random
import time

def fill(n):
    return [random.randint(0,1000) for i in range(n)]

def nej(l):
    biggest = l[0]
    for i in l:
        if i > biggest:
            biggest = i

    return biggest

def druhejnej(l):
    biggest = nej(l)
    biggest2 = 0
    for i in l:
        if i < biggest and i > biggest2:
            biggest2 = i
    return biggest2

def delitelna(l, d):
    return [i for i in l if not i%d]

def suma(l):
    out = l[0]
    for i in l[1:]:
        out += i
    return out

def avg(l):
    s = l[0]
    n = 1
    for i in l[1:]:
        s += i
        n += 1

    return s/n

def quicksort(l):
    if len(l) <= 1:
        return l
    
    pivot = random.choice(l)

    bigger = []
    smaller = []
    pivotList = []

    for i in l:
        if i > pivot:
            bigger.append(i)
        if i < pivot:
            smaller.append(i)
        if i == pivot:
            pivotList.append(i)

    return quicksort(bigger) + pivotList + quicksort(smaller)

def mergesort(l):
    def merge(l1, l2):
        c= []
        while len(l1) != 0 and len(l2) != 0:
            if l1[0] > l2[0]:
                c.append(l1[0])
                l1.pop(0)
            else:
                c.append(l2[0])
                l2.pop(0)
        c.extend(l1+l2)
        return c
    lol = [[i] for i in l]
    newLol = []
    while len(lol) > 1:
        for index, item in enumerate(lol):
            if not index%2:
                if index < len(lol)-1:
                    newLol.append(merge(item,lol[index+1]))
                else:
                    newLol.append(item)
        lol = newLol
        newLol = []
    return lol[0]

def mergesortWrong(l):
    def merge(l1, l2):
        c= []
        while len(l1) != 0 and len(l2) != 0:
            if l1[0] > l2[0]:
                c.append(l1[0])
                l1.pop(0)
            else:
                c.append(l2[0])
                l2.pop(0)
        c.extend(l1+l2)
        return c
    lol = [[i] for i in l]
    newList = []
    while len(newList) < len(l):
        newList = merge(lol[0], newList)
        lol.pop(0)
    return newList

def selectionsort(l):
    for i in range(len(l)):
        biggest = l[i:][0]
        biggestIndex = i
        for index, item in enumerate(l):
            if item > biggest:
                biggest = item
                biggestIndex = index
        l.insert(0,biggest)
        l.pop(biggestIndex+1)
    return l

def bublesort(l):
    for i in range(len(l)):
        for index, item in enumerate(l):
            try:
                if item < l[index+1]:
                    l[index], l[index+1] = l[index+1], l[index]
            except IndexError:
                pass
    return l

def insertionsort(l):
    for index, item in enumerate(l):
        if index == 0:
            continue
        if item > l[index-1]:
            changed = False
            for i, item_ in enumerate(reversed(l[:index])):
                if item < item_:
                    l.insert(index-i, item)
                    l.pop(index+1)
                    changed = True
                    break
            if not changed:
                l.insert(0, item)
                l.pop(index+1)
    return l


# Nejprve jsem si řekl, že udělám quicksort, když jste o něm tak mluvil, tak jsem si myslel, že to bude něco složitého.
# To ale nebyl ten případ. Bylo to velice jednoduché. Tak jsem se vrhl na mergesort, ale ten je nějak neefektivní a trvá o hodně déle než quicksort.
# Následně jsem slyšel Bohouše a Vladana, že dělají selcetionsort, tak jsem ho udělal taky. A pak jsem si řekl, že když už jsem u toho, tak udělám i
# bublesort a insertion sort.

start = time.time()
a = fill(100000)
print(time.time()-start)
start= time.time()
quicksort(a)
print(time.time()-start)
start= time.time()
mergesort(a)
print(time.time()-start)