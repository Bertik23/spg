def nsd(a,b):
    u,w = a,b
    while w != 0:
        r = u%w
        u = w
        w = r
    return u

class Zlomek:
    def __init__(self, citatel, jmenovatel):
        self.citatel = citatel
        self.jmenovatel = jmenovatel
        self.zkratit()

    def __str__(self):
        return f"{self.citatel}/{self.jmenovatel}"

    def zkratit(self):
        d = nsd(self.citatel, self.jmenovatel)
        self.citatel //= d
        self.jmenovatel //= d
        self.citatel, self.jmenovatel = int(self.citatel), int(self.jmenovatel)
    
    def __add__(self, other):
        if type(other) in (int, float):
            out = Zlomek(self.citatel + self.jmenovatel * other, self.jmenovatel)
        elif type(other) == Zlomek:
            out = Zlomek(self.citatel*other.jmenovatel + other.citatel*self.jmenovatel, self.jmenovatel*other.jmenovatel)
        else:
            otherType = str(type(other)).split('\'')[1]
            raise TypeError(f"unsupported operand type(s) for +: 'Zlomek' and '{otherType}'")
        out.zkratit()
        return out


    def __neg__(self):
        return Zlomek(-self.citatel, self.jmenovatel)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        if type(other) in (int, float):
            out = Zlomek(self.citatel*other,self.jmenovatel)
        elif type(other) == Zlomek:
            out = Zlomek(self.citatel*other.citatel,self.jmenovatel*other.jmenovatel)
        else:
            otherType = str(type(other)).split('\'')[1]
            raise TypeError(f"unsupported operand type(s) for *: 'Zlomek' and '{otherType}'")
        out.zkratit()
        return out

    def __truediv__(self, other):
        if type(other) in (int,float):
            return self * (1/other)
        elif type(other) == Zlomek:
            return self * Zlomek(other.jmenovatel, other.citatel)


