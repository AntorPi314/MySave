# 1. Even-Odd Summary
"""
Write a function that takes any number of integers using *args and returns a dictionary with
counts, sums, and lists of even and odd numbers separately. Use list comprehensions and
conditions.
"""

def summarize(*args):
    return {
        "frequency": {i: args.count(i) for i in set(args)},     # ///////////////////////////
        "sum": sum(args),
        "even": [i for i in args if i % 2 == 0],
        "odd": [i for i in args if i % 2 != 0]
    }

print(summarize(1, 2, 3, 3, 4, 5, 6))


# Output: {'frequency': {1: 1, 2: 1, 3: 2, 4: 1, 5: 1, 6: 1}, 'sum': 24, 'even': [2, 4, 6], 'odd': [1, 3, 3, 5]}




# 2. Nested List Flattening
"""
Write a function that accepts a list of lists with numbers and strings, flattens it into a single list,
separates numbers and strings into a tuple of two lists, and returns their sums/concatenation.
Use loops, type checking, and comprehensions.
"""

def flatten_and_process(nested_list):
    flat = [item for sub in nested_list for item in sub]
    numbers = [x for x in flat if type(x) in (int, float)]
    strings = [x for x in flat if type(x) == str]
    # joinString = ""
    # for i in strings: joinString += i
    # joinString = "".join(strings)
    return (numbers, strings), sum(numbers), "".join(strings)    # /////////////////////

print(flatten_and_process([[1, "a"], [2, "b", 3], ["c"]]))

# Output: ([1, 'a', 2, 'b', 3, 'c'], [1, 2, 3], ['a', 'b', 'c'], 6, 'abc')



# 3. Custom Filter and Map
"""
Write a function that takes a list and a function as a parameter. It should filter out negative
numbers, apply the function to the remaining numbers, and return a tuple of the original
filtered list and the transformed list.
"""

def filter_and_transform(lst, func):
    filtered = [x for x in lst if x >= 0]
    transformed = [func(x) for x in filtered]
    return filtered, transformed

print(filter_and_transform([-2, 3, -5, 6, 0], lambda x: x * 2))    # ///////////////////

# Output: ([3, 6, 0], [6, 12, 0])




# 4. Word Length Analysis
"""
Write a function that takes a string sentence and counts words of length >3, finds unique
words, and returns a dictionary mapping word lengths to lists of words. Use dict
comprehension and split().
"""

def word_analysis(sentence):
    words = sentence.split()
    unique_words = set(words)
    long_words_count = len([w for w in words if len(w) > 3])

    # length_map = {}
    # for w in words:
    #     l = len(w)
    #     if l not in length_map:
    #         length_map[l] = []
    #     length_map[l].append(w)

    length_map = {len(uw): 
                  [w for w in words if len(w) == len(uw)]
                   for uw in unique_words
                 }

    return length_map

print(word_analysis("this is a simple simple test case for word analysis"))

# Output Example: (5, {'this', 'simple', ...}, {4: ['this', 'test', 'case', 'word'], 6: ['simple', 'simple'], ...})





# 5. Generator Pipeline
"""
Create a generator that yields squares of numbers divisible by 3 from 1 to N. Then write a
function that consumes the generator to return the sum of numbers ending with 9. Use
generator expressions inside loops.
"""

def square_gen(N):
    for i in range(1, N+1):
        if i % 3 == 0:
            yield i * i

def sum_ending_with_9(N):
    return sum([x for x in square_gen(N) if x % 10 == 9])

print(sum_ending_with_9(50))

# Output Example: 1827





# 6. Function with *args and **kwargs
"""
Write a function that accepts *args (numbers) and **kwargs (options like
operation='sum' or 'product'). Perform the operation on the numbers and return the
result. Use loops, conditions, and function as parameter for extra operations.
"""

def operate_numbers(*args, **kwargs):
    operation = kwargs["operation"]
    result = 1 if operation == "product" else 0

    for num in args:
        if operation == "sum":
            result += num
        elif operation == "product":
            result *= num

    return result

print(operate_numbers(1, 2, 3, 4, operation="sum"))
print(operate_numbers(1, 2, 3, 4, operation="product"))

# Output:
# 10
# 24





# 7. Unique Character Counter
"""
Write a function that takes a list of strings, returns a dictionary mapping each string to a set
of its unique characters, and also returns the total unique characters across all strings.
Use loops and set operations.
"""

def unique_char_counter(strings):
    mapping = {s: set(s) for s in strings}     # ////////////////////////////
    total_unique = set("".join(strings))
    return mapping, total_unique, len(total_unique)

print(unique_char_counter(["apple", "banana", "cat"]))

# Output Example:
# ({'apple': {'a', 'p', 'l', 'e'}, 'banana': {...}, 'cat': {...}}, {'a','p','l','e','b','n','c','t'}, 8)





# 8. Nested Dictionary Merge
"""
Write a function that takes multiple dictionaries as *args. Merge them into one dictionary, and
for conflicting keys, keep the max value. Return the merged dictionary and a list of
conflicts.
"""

def merge_dicts(*dicts):   # /////////////////////////
    merged = {}
    conflicts = set()

    for d in dicts:
        for k,v in d.items():
            if k in merged:
                conflicts.add(k)
                merged[k] = max(merged[k], v)
            else:
                merged[k] = v

    return merged, list(conflicts)

print(merge_dicts({"a": 5, "b": 2}, {"a": 7, "c": 3}, {"b": 10}, {"b": 15}))

# Output:
# ({'a': 7, 'b': 10, 'c': 3}, ['a', 'b'])





# 9. Advanced Comprehension
"""
Given a list of numbers and strings, create a single dictionary where keys are numbers
squared (numbers only) and values are uppercase strings (strings only). Ignore mismatched
types. Use dictionary comprehension with conditions.
"""

# def advanced_comprehension(mixed_list):
#     nums = [x for x in mixed_list if type(x) in (int, float)]
#     strs = [x for x in mixed_list if type(x) == str]
#     return {n*n: s.upper() for n, s in zip(nums, strs)}

def advanced_comprehension(mixed_list):
    nums = [x for x in mixed_list if type(x) in (int, float)]
    strs = [x for x in mixed_list if type(x) == str]

    # only zip on equal count pairs
    limit = min(len(nums), len(strs))
    return {nums[i] * nums[i]: strs[i].upper() for i in range(limit)}

print(advanced_comprehension([2, "a", 3, "b", 4, "hello"]))

# Output:
# {4: 'A', 9: 'B', 16: 'HELLO'}





# 10. Fibonacci Filter
"""
Write a function that generates the first N Fibonacci numbers using a generator and returns a
list of only prime Fibonacci numbers. Use loops, generator, and a helper function for
primality.
"""

from sympy import isprime

def fib_gen(N):
    a, b = 0, 1
    for i in range(N):
        yield a
        a, b = b, a + b

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def prime_fibo(N):
    return [x for x in fib_gen(N) if isprime(x)]

print(prime_fibo(15))

# Output Example: [2, 3, 5, 13, 89, ...]





# 11. Multi-Level Sorting
"""
Write a function that accepts a list of tuples (name, age, score). Return a list of names
sorted first by score descending, then age ascending. Use sorted() with lambda, loops,
and tuple unpacking.
"""

def sort_students(data):
    sorted_data = sorted(data, key=lambda x: (-x[2], x[1]))  # ///////////////////////
    return [name for name, age, score in sorted_data]

print(sort_students([("John", 20, 90), ("Alice", 22, 95), ("Bob", 19, 95), ("Mike", 21, 85)]))

# Output: ['Alice', 'Bob', 'John', 'Mike']





# 12. Text Transformation Pipeline
"""
Write a function that takes a list of sentences and multiple functions as *args. Each function
should transform the text (like lowercasing, replacing spaces with underscores, removing
vowels). Return a list of transformed sentences after all functions applied.
"""

def transform_text(sentences, *funcs):
    result = []
    for sentence in sentences:
        for func in funcs:
            sentence = func(sentence)      # ////////////////////////
        result.append(sentence)
    return result

# Example transformer functions
# lower = lambda s: s.lower()
def lower(s):
    return s.lower()

underscore = lambda s: s.replace(" ", "_")
remove_vowels = lambda s: ''.join([ch for ch in s if ch not in "aeiouAEIOU"]) # //////////////////////

print(transform_text(["Hello World", "Python Coding"], lower, underscore, remove_vowels))

# Output: ['hll_wrld', 'pythn_cdng']





# 13. Set Operations Analyzer
"""
Write a function that takes two lists and returns:
● Intersection as a set
● Symmetric difference as a tuple
● Union count
Use set operations, comprehension, loops, and tuple/list conversions.
"""

def analyze_sets(list1, list2):          #  /////////////////////////
    s1, s2 = set(list1), set(list2)
    intersection = s1 & s2
    symmetric_diff = tuple(s1 ^ s2)
    union_count = len(s1 | s2)
    return intersection, symmetric_diff, union_count

print(analyze_sets([1, 2, 3, 4], [3, 4, 5, 6]))

# Output: ({3, 4}, (1, 2, 5, 6), 6)





# 14. Multi-Level Average
"""
Given a dictionary of class names mapping to lists of student scores, write a function that
returns a dictionary mapping class to average, and overall class average. Use loops,
comprehension, and multiple return.
"""

def class_average(data):
    class_avg = {cls: sum(scores) / len(scores) for cls, scores in data.items()}
    overall_avg = sum(class_avg.values()) / len(class_avg)
    return class_avg, overall_avg

print(class_average({"ClassA": [80, 90, 85], "ClassB": [70, 75, 78], "ClassC": [88, 92]}))

# Output Example: ({'ClassA': 85.0, 'ClassB': 74.33, 'ClassC': 90.0}, 83.11)





# 15. Function Decorator Simulation
"""
Write a function that accepts another function and prints start and end timestamps whenever
the function runs. Use function as parameter, *args, **kwargs, and loops inside the
function if necessary for multiple runs.
"""

import time

def run_with_timestamp(func, *args, **kwargs):
    print("Start:", time.strftime("%H:%M:%S"))
    result = func(*args, **kwargs)
    print("End:", time.strftime("%H:%M:%S"))
    return result

def sample_task(n):
    s = 0
    for i in range(n):
        s += i
    return s

print(run_with_timestamp(sample_task, 1000000))

# Output Example:
# Start: 12:30:05
# End: 12:30:05
# 499999500000
