

tou = (1, 2, 3, 40, 5, 6, 7, 8, 9, 10)
list = [1, 2, 30, 4, 5, 6, 7, 8, 9, 10]



from functools import reduce


num = [1, 3, 4, 5, 8, 4]

print(reduce(lambda x, y: x+y, num))


def add(a: int, b: float):
    '''add two number'''
    return a + b

print(add.__doc__)

print(add(2, 3.5))



def decorator(func):
    def wrapper():
        print("Before function")
        func()
        print("After function")
    return wrapper

@decorator
def hello():
    print("Hello!")

hello()



def add2(a, b):
    x = 20
    def sum():
        nonlocal x
        x = 10
        return a + b + x
    
    return sum

print(add2(2, 3)())