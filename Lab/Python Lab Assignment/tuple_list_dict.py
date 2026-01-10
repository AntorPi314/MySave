###############################
########## Tuple ##############
###############################

t = (1, 2, 3, 2, 4)

# count(x) → কতবার আছে
print("count of 2:", t.count(2))  # 2

# index(x[, start[, end]]) → প্রথম index
print("index of 3:", t.index(3))  # 2




###############################
########## List ###############
###############################

lst = [3, 1, 4, 1, 5]

# append(x) → শেষ এ যোগ
lst.append(9)
print("append:", lst)  # [3, 1, 4, 1, 5, 9]

# extend(iterable) → একাধিক যোগ
lst.extend([6, 7])
print("extend:", lst)  # [3, 1, 4, 1, 5, 9, 6, 7]

# insert(i, x) → index i তে x যোগ
lst.insert(2, 10)
print("insert at 2:", lst)  # [3, 1, 10, 4, 1, 5, 9, 6, 7]

# remove(x) → প্রথম occurrence মুছে দেয়
lst.remove(1)
print("remove 1:", lst)  # [3, 10, 4, 1, 5, 9, 6, 7]

# pop([i]) → index i থেকে remove & return
print("pop index 3:", lst.pop(3))  # 1
print("after pop:", lst)  # [3, 10, 4, 5, 9, 6, 7]

# clear() → সব remove
# lst.clear()

# index(x[, start[, end]]) → index খুঁজে দেয়
print("index of 9:", lst.index(9))  # 4

# count(x) → কতবার আছে
print("count of 4:", lst.count(4))  # 1

# sort(key=None, reverse=False)
lst.sort()
print("sort:", lst)  # [3, 4, 5, 6, 7, 9, 10]

# reverse() → লিস্ট reverse
lst.reverse()
print("reverse:", lst)  # [10, 9, 7, 6, 5, 4, 3]

# copy() → shallow copy
lst_copy = lst.copy()
print("copy:", lst_copy)  # [10, 9, 7, 6, 5, 4, 3]




###############################
########## Dict ###############
###############################


d = {"name": "Antor", "age": 22}

# get(key[, default]) → value নেয়, না থাকলে default
print("get name:", d.get("name"))  # Antor
print("get city:", d.get("city", "Dhaka"))  # Dhaka

# keys() → সব keys
print("keys:", d.keys())  # dict_keys(['name', 'age'])

# values() → সব values
print("values:", d.values())  # dict_values(['Antor', 22])

# items() → সব key-value pair
print("items:", d.items())  # dict_items([('name', 'Antor'), ('age', 22)])

# pop(key[, default]) → key remove & return
print("pop age:", d.pop("age"))  # 22
print("after pop:", d)  # {'name': 'Antor'}

# popitem() → last inserted pair remove & return
d["country"] = "BD"
print("popitem:", d.popitem())  # ('country', 'BD')
print("after popitem:", d)  # {'name': 'Antor'}

# update(other_dict) → merge dict
d.update({"age": 22, "city": "Dhaka"})
print("update:", d)  # {'name': 'Antor', 'age': 22, 'city': 'Dhaka'}

# clear() → সব empty
# d.clear()

# copy() → shallow copy
d_copy = d.copy()
print("copy:", d_copy)  # {'name': 'Antor', 'age': 22, 'city': 'Dhaka'}

# setdefault(key[, default]) → যদি না থাকে, default set করে
d.setdefault("country", "BD")
print("setdefault:", d)  # {'name': 'Antor', 'age': 22, 'city': 'Dhaka', 'country': 'BD'}




###############################
########## Set ###############
###############################

s = {1, 2, 3, 4, 2}

# add(x) → element যোগ
s.add(5)
print("add 5:", s)  # {1, 2, 3, 4, 5}

# update(iterable) → একাধিক element যোগ
s.update([6, 7, 1])
print("update [6,7,1]:", s)  # {1, 2, 3, 4, 5, 6, 7}

# remove(x) → element remove, না থাকলে error
s.remove(3)
print("remove 3:", s)  # {1, 2, 4, 5, 6, 7}

# discard(x) → element remove, না থাকলেও error দেয় না
s.discard(10)
print("discard 10 (no error):", s)  # {1, 2, 4, 5, 6, 7}

# pop() → random element remove & return
popped = s.pop()
print("pop:", popped)
print("after pop:", s)

# clear() → সব remove
# s.clear()

# copy() → shallow copy
s_copy = s.copy()
print("copy:", s_copy)

# union(other_set) → sets মিলিয়ে নতুন set
s2 = {5, 6, 8}
print("union:", s.union(s2))  # {1,2,4,5,6,7,8}

# intersection(other_set) → common elements
print("intersection:", s.intersection(s2))  # {5,6}

# difference(other_set) → s-others
print("difference:", s.difference(s2))  # elements in s but not in s2

# symmetric_difference(other_set) → elements in s or s2 but not both
print("symmetric_difference:", s.symmetric_difference(s2))  # {1,2,4,7,8}

# issubset(other_set) → s ⊆ other?
print("issubset:", s.issubset({1,2,4,5,6,7,8}))  # True or False

# issuperset(other_set) → s ⊇ other?
print("issuperset:", s.issuperset({5,6}))  # True

# isdisjoint(other_set) → কোন common element নেই?
print("isdisjoint:", s.isdisjoint({8,9}))  # True
