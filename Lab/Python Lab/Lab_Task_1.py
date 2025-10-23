# Solving-1
def analyze_marks(*marks, passing=40):
    passed = [m for m in marks if m >= passing]
    failed = [m for m in marks if m < passing]
    return passed, failed

passed, failed = analyze_marks(30, 45, 90, 60, 25)
print(f"Output-1> Passed: {len(passed)}, Failed: {len(failed)}")


# Solving-2
def word_stats(sentence, top_n=3):
    words = sentence.lower().split()
    freq = {w: words.count(w) for w in set(words)}
    top_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:top_n]
    return top_words

top_words = word_stats("hi hi hi hello world hello you you")
print(f"Output-2> Top {len(top_words)} words: {top_words}")


# Solving-3
def unique_sorted(numbers):
    unique_nums = sorted(set(numbers))
    total = sum(unique_nums)
    avg = total / len(unique_nums)
    return tuple(unique_nums), total, avg

unique_nums, total, avg = unique_sorted([1, 3, 2, 3, 6, 4, 5])
print(f"Output-3> Unique numbers: {unique_nums}, Total: {total}, Average: {avg}")


# Solving-4
def transform_list(data, func):
    return [func(x) for x in data]

result = transform_list([1, 2, 3, 4], lambda x: x**2 if x % 2 == 0 else x)
print("Output-4> " + str(result))


# Solving-5
def build_contacts(**contacts):
    vowel_contacts = {k: v for k, v in contacts.items() if k[0].lower() in 'aeiou'}
    return len(contacts), vowel_contacts

result = build_contacts(Antor="017", Jon="018", Eva="019", Omar="016")
print("Output-5> " + str(result))



# Solving-6
def summarize_records(records):
    avg_scores = {name: sum(scores) / len(scores) for name, scores in records}
    return avg_scores

records = [('Antor', [10, 20, 30]), ('Bob', [5, 15]), ('Eva', [100])]
result = summarize_records(records)
print("Output-6> " + str(result))


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


# Solving-8
def mixed_comprehension(data):
    squared_nums = [x**2 for x in data if isinstance(x, int)]
    upper_strs = {x.upper() for x in data if isinstance(x, str)}
    return squared_nums, upper_strs

nums, strs = mixed_comprehension([1, 2, 'hi', 3, 'bye', 4])
print(f"Output-8> Numbers: {nums}, Strings: {strs}")


# Solving-9
def summary(name, **info):
    details = ', '.join(f"{k}={v}" for k, v in info.items())
    result = f"{name}: {details}"
    if 'country' in info:
        result += f" (from {info['country']})"
    return result

result = summary("Antor", age=22, country="Bangladesh", hobby="Coding")
print("Output-9> " + result)


# Solving-10
def pipeline(numbers, *funcs):
    for func in funcs:
        numbers = [func(x) for x in numbers]
    return numbers

def inc(x): return x + 1
def double(x): return x * 2

result = pipeline([1, 2, 3], inc, double)
print("Output-10> " + str(result))



