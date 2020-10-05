import typing

def kvadrat(a: float, b: float = 0.0, c: float = 0.0) -> typing.Union[None,float,typing.Tuple[float,float]]:
    """Vypočítá nulové body kvadratické rovnice s pomocí radaných parametrů

    Parametry
    ---------
    ::
        a: float
        b: float
        c: float
    
    Výstup
    ------
    ::
        None, float nebo (float, float)"""
    for i in (a,b,c):
        if type(i) not in (float,int):
            raise TypeError(f"Parametry kvadratické rovnice musí být číslo. Nesmí být {type(i)}")
    if a == 0:
        raise ValueError("Nemůžeš počítat lineární rovnici pomocí diskriminantu pro kvadratickou rovnici")
    D = b**2 - 4*a*c
    if D < 0:
        return None
    x1, x2 = (-b + D**0.5)/(2*a), (-b - D**0.5)/(2*a)
    if x1 == x2:
        return x1
    else:
        return x1, x2