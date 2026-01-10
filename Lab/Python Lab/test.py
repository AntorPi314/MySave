

# (1) Write a function that takes any number of integers using *agrs and returns dictionary 
# with counts, sums and list of even and odd number separately. Use list compreshensions
# and conditions

def summerize(*agrs):
    dict = {n: agrs.count(n) for n in agrs}
    _sum = sum(agrs)
    evenList = [n for n in agrs if n%2 == 0]
    oddList = [n for n in agrs if n%2 != 0]
    return dict, _sum, evenList, oddList

print(summerize(1,2,3,7,11))


def fil_trans(list, func):
    filtered = [n for n in lst if n >= 0]
    transformed = [func for x in filtered]
    return filtered, transformed


print([1,2,3], lambda x: x**2)