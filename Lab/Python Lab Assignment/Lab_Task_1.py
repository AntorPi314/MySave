list = [2, 3, 5, 7, 1]
lists = sorted(list, key=lambda x: x, reverse=True)


# 1. Student Marks Analyzer 
"""
Write a function analyze_marks(*marks, passing=40) that: 
● Takes variable-length marks using *args. 
● Returns two lists — one for passed and one for failed marks. 
● Use list comprehension and a condition to separate them. 
● Print a short summary using an f-string.
"""

# Solving-1
def analyze_marks(*marks, passing=40):
    passed = [m for m in marks if m >= passing]
    failed = [m for m in marks if m < passing]
    return passed, failed

passed, failed = analyze_marks(30, 45, 90, 60, 25)
print(f"Output-1> Passed: {len(passed)}, Failed: {len(failed)}")



# 2. Word Frequency Counter     ///////////////////////////////////////
"""
Define a function word_stats(sentence, top_n=3) that: 
● Converts the sentence into lowercase and splits it into words. 
● Uses a dictionary to count word frequencies. 
● Returns the top n frequent words as a list of tuples (word, count). 
● Use a dictionary comprehension and sorted() with lambda. 
"""
# Solving-2
def word_stats(sentence, top_n=3):
    words = sentence.lower().split()
    freq = {w: words.count(w) for w in set(words)}
    freq_tuple_list = [(k, v)  for k,v in freq.items()]
    top_n_word = sorted(freq_tuple_list, key=lambda x: x[1], reverse=True)
    return top_n_word[:top_n]

top_words = word_stats("hi hi hi hello world hello you you")
print(f"Output-2> Top {len(top_words)} words: {top_words}")



# 3. Unique Sorted Numbers 
"""
Create a function unique_sorted(numbers) that: 
● Removes duplicates using a set. 
● Returns a tuple of sorted values. 
● Also return the sum and average as multiple return values. 
"""
# Solving-3
def unique_sorted(numbers):
    unique_nums = sorted(set(numbers))
    total = sum(unique_nums)
    avg = total / len(unique_nums)
    return tuple(unique_nums), total, avg

unique_nums, total, avg = unique_sorted([1, 3, 2, 3, 6, 4, 5])
print(f"Output-3> Unique numbers: {unique_nums}, Total: {total}, Average: {avg}")




# 4. Transform Data with Function Parameter    /////////////////////////////
"""
Write a function transform_list(data, func) that: 
● Takes a list and a function as a parameter. 
● Applies func to each element using list comprehension. 
● Test it with a lambda like lambda x: x**2 if x % 2 == 0 else x. 
"""
# Solving-4
def transform_list(data, func):
    return [func(x) for x in data]

result = transform_list([1, 2, 3, 4], lambda x: x**2 if x % 2 == 0 else x)
print("Output-4> " + str(result))




# 5. Contact Directory ////////////////////////// 
"""
Define build_contacts(**contacts) where keys are names and values are phone 
numbers. 
Then filter only contacts whose names start with vowels using a dict comprehension. 
Return both total contacts and vowel-starting contacts. 
"""
# Solving-5
def build_contacts(**contacts):
    vowel_contacts = {k: v for k, v in contacts.items() if k[0].lower() in 'aeiou'}
    return len(contacts), vowel_contacts

result = build_contacts(Antor="017", Jon="018", Eva="019", Omar="016")
print("Output-5> " + str(result))




# 6. Nested Structure Summary 
"""
Given a list of tuples like: 
records = [('Antor', [10, 20, 30]), ('Bob', [5, 15]), ('Eve', [100])] 
Write a function that returns a dictionary where each name maps to the average of their list 
using for loops and comprehension.
"""
# Solving-6
def summarize_records(records):
    avg_scores = {name: sum(scores)/len(scores) for name, scores in records}
    return avg_scores

records = [('Antor', [10, 20, 30]), ('Bob', [5, 15]), ('Eva', [100])]
result = summarize_records(records)
print("Output-6> " + str(result))




# 7. Fibonacci Generator    ///////////////////////////
"""
Create a generator function fib(limit) that yields Fibonacci numbers up to limit. 
Use it inside another function even_fib_sum(limit) that: 
● Consumes the generator using a for loop 
● Returns the sum of only even Fibonacci numbers. 
"""
# Solving-7
def fib(limit):
    a, b = 0, 1
    while a <= limit:
        yield a
        a, b = b, a + b

def even_fib_sum(limit):
    total = 0
    for n in fib(limit):
        if n % 2 == 0:
            total += n
    return total

result = even_fib_sum(100)
print("Output-7> " + str(result))




# 8. Mixed Comprehension Challenge 
"""
Given a list of mixed data like [1, 2, 'hi', 3, 'bye', 4], 
use list comprehension to create: 
● A list of squared numbers. 
● A set of strings converted to uppercase. 
Return both using multiple return values. 
"""
# Solving-8
def mixed_comprehension(data):
    # squared_nums = [x**2 for x in data if isinstance(x, int)]
    squared_nums = [x**2 for x in data if type(x) == int]
    upper_strs = {x.upper() for x in data if type(x) == str}   #//////////////////////////
    return squared_nums, upper_strs

nums, strs = mixed_comprehension([1, 2, 'hi', 3, 'bye', 4])
print(f"Output-8> Numbers: {nums}, Strings: {strs}")




# 9. Keyword Summary Function 
"""
Write summary(name, **info) that: 
● Accepts a name and multiple keyword arguments like age=25, country='BD'. 
● Builds a summary string using a loop and f-string. 
● If country key exists, append a note like "from Bangladesh". 
Return the summary. 
"""
# Solving-9
def summary(name, **info):
    details = [f"{k}={v}" for k, v in info.items()]   # //////////////////////////////
    details = ", ".join(details)
    result = f"{name}: {details}"
    if 'country' in info:
        result += f" (from {info['country']})"
    return result

result = summary("Antor", age=22, country="Bangladesh", hobby="Coding")
print("Output-9> " + result)




# 10. Filter and Transform Pipeline 
"""
Define pipeline(numbers, *funcs) that: 
● Takes a list and multiple functions (*args style). 
● Applies each function in order to transform the list. 
● Use for loops, conditions, and list comprehension together. 
Example: 
def inc(x): return x+1   
def double(x): return x*2   
print(pipeline([1,2,3], inc, double))  # → [4,6,8] 
"""
# Solving-10
def pipeline(numbers, *funcs):
    for func in funcs:
        numbers = [func(x) for x in numbers]     # //////////////////////////////////////
    return numbers

def inc(x): return x + 1
def double(x): return x * 2

result = pipeline([1, 2, 3], inc, double)
print("Output-10> " + str(result))



