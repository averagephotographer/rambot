from time import time,sleep
from hashlib import sha256,md5
SALT = "goodluck;)"
EPOCH = 1585105810
DURATION = 20
SELECTION = [12,3,19,6,10,24,18,5,20,15]

def lock():
    t = time()
    t = str(int(t-(t%DURATION))-EPOCH)+SALT
    t = t.encode('utf-8')
    h = sha256(t).hexdigest()
    h = md5(h.encode('utf-8')).hexdigest()
    h=str(h)
    code = ""
    for i in range(0,len(SELECTION),2):
        character = h[SELECTION[i]]+h[SELECTION[i+1]]
        #62 possible characters, starting at ascii 28='0'
        character = int(character,16)%62+48
        if character > 57: character+=7
        if character > 91: character+=6
        code+=chr(character)
    return code
    
    
print(lock())
