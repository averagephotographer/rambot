

def interp(aLo,aHi,aTar,bLo,bHi):
    aHi = float(aHi)
    aLo = float(aLo)
    aTar = float(aTar)
    bHi = float(bHi)
    bLo = float(bLo)
    part = ((aTar-aLo)/(aHi-aLo))
    bTar = bLo+((bHi-bLo)*part)
    return str(bTar)
