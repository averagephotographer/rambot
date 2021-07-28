from time import time,sleep
from hashlib import sha256,md5
SALT = "goodluck;)"
EPOCH = 1585105810
DURATION = 9
SELECTION = [12,3,19,6,10]

def lock():
    t = time()
    t = str(int(t-(t%DURATION))-EPOCH)+SALT
    t = t.encode('utf-8')
    h = sha256(t).hexdigest()
    h = md5(h.encode('utf-8')).hexdigest()
    code = ""
    for i in SELECTION:
        code+=str(h)[i]
    return code
    
    
