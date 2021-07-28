

def bigArgs(a,b,*args,**kwargs):
    print("a: {} b: {}".format(a,b))
    print("args:")
    for i in args:
        print(i)
    print("kwargs:")
    for name,value in kwargs.items():
        print(name + " = " + value)

bigArgs("hello","world",1,2,3,4,thing1="milk",thing2="eggs")
