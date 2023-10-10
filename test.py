import random


def f(x):
    if (x == 0):
        raise Exception("HUY")

for i in range(10):
    x = random.randint(0, 1)
    print(x)
    try:
        f(x)
    except Exception as error:
        print(error.args == Exception("HUY").args)