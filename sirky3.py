sirky = 5

tree = {}
hrac = 4
def play(sirky):
    global hrac
    hrac += 1
    hrac = hrac%3+1
    print(hrac, sirky)
    if sirky == 1 and hrac == 3:
        print(sirky,hrac)
        return False
    if sirky>0:
        for i in range(1,4):
            if play(sirky-i):
                continue
            else:
                if sirky not in tree.keys():
                    tree[sirky] = []
                tree[sirky].append(i)
            
    
play(sirky)
print(tree) 