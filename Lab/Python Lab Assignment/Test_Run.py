list = [2, 3, 5, 7, 1]
tuples = (2, 3, 5, 7)
s = "Antor"
print(set(s))

dicts = {}

dicts["A"] = 2


def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


print(is_prime(2))

