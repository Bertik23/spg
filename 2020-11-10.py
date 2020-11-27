def napln(n):
    return [i for i in range(1,n+1)]

def rozpocitavadlo(l, n):
    out = []
    i = 0
    a = 0
    while len(l) > 0:
        a += 1
        if i >= len(l):
            i = 0
        if a == n:
            out.append(l.pop(i))
            a = 0
            i-=1
        i += 1
    return out

print(rozpocitavadlo(napln(6),5))
