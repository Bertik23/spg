def fromDHMtoH(d: float, h: float, m: float) -> float:
    """Převede čas ve formátu d,h,m na hodiny.

    Parametry
    ---------
    ::
        d: float - dny
        h: float - hodiny
        m: float - minuty

    Výstup
    ------
    ::
        float - hodiny
    """
    for i in (d,h,m):
        if type(i) not in (float, int):
            raise TypeError(f"Čas musí být číslo, nesmí být {type(i)}") 

    return d*24+h+(m/60)

while True:
    print(f"Váš zapsaný čas je: {fromDHMtoH(float(input('Dní: ')), float(input('Hodin: ')), float(input('Minut: ')))} hodin")