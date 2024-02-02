y = 3
x = 2 + y

def factorial(x):
    if x == 0:
        return 1
    else:
        return x * factorial(x - 1)

print(factorial(5))
