############################################################
############### Python Lab (Assignment) ####################
############################################################
##### Name: Antor Hawlader
##### ID: 222071024
##### Batch: 30th
##### Semester: 9th
##### CSE-4115: Python Programming Language
############################################################



# PROBLEM 1: List Comprehension Basics
"""
Given a list of numbers, create two new lists using list comprehension:
- One containing only even numbers
- One containing only odd numbers
Then print the count of each.
"""
numbers = [12, 7, 23, 45, 18, 9, 34, 56, 3, 28]

# Your solution here:

even_nums = [e for e in numbers if e%2 == 0]
odd_nums = [o for o in numbers if o%2!=0]

print(f'Even Count: {len(even_nums)}')
print(f'Odd Count: {len(odd_nums)}')


# PROBLEM 2: Filtering with List Comprehension
"""
A library tracks book pages. Create two lists:
- Books with less than 300 pages
- Books with 300 or more pages
"""
book_pages = [450, 280, 150, 320, 200, 500, 180, 390]

# Your solution here

book_less_300 = [b for b in book_pages if b < 300]
book_greater_300 = [b for b in book_pages if b >= 300]
print(book_less_300, book_greater_300)



# PROBLEM 3: Function Returning Dictionary with Statistics
"""
Write a function that takes two lists (passed_students, failed_students) 
and returns a dictionary containing:
- Average score of passed students
- Average score of failed students
- Percentage of passed students
- Percentage of failed students
"""
passed = [75, 82, 90, 68, 85]
failed = [45, 38, 52, 48]

# Your solution here:

def calculate_stats(passed, failed):
    total_passed = len(passed)
    total_failed = len(failed)
    total_student = total_passed + total_failed
    statistics_dict = {
        "Average_Passed_Score": sum(passed)/total_passed,
        "Average_Failed_Score": sum(failed)/total_failed,
        "Passed_percentage": round((total_passed/total_student)*100, 2),
        "Failed_percentage": round((total_failed/total_student)*100, 2)
    }
    return statistics_dict

print(calculate_stats(passed, failed))



# PROBLEM 4: Understanding Data Structures
"""
Create examples of:
- A list to store monthly sales (can have duplicates, order matters)
- A tuple to store geographic coordinates (immutable)
- A set to store unique employee IDs
- A dictionary to store product info (ID as key, details as value)
Explain when to use each.
"""

# Your solution here

sales = [200, 300, 150, 200]
# Use a list when we need to keep the order of items or allow reapeated values.

coordinates = (40.7128, -74.0060)
# Use a tuple when the data should not change

employee_ids = {101, 102, 103}
# Use a set when we need to ensure all items are unique.

products = {1: "Laptop", 2: "Mouse"}
# Use a dictionary when we want to map keys to values for fast lookup.




# PROBLEM 5: Dictionary Comprehension
"""
Given a dictionary of product quantities, create a new dictionary
that only includes products with quantity greater than 50.
"""
inventory = {"apples": 120, "bananas": 30, "oranges": 80, "grapes": 45, "melons": 65}

# Your solution here:

high_stock = {k: v for k,v in inventory.items() if v > 50}



# PROBLEM 6: Calculating Averages in Nested Dictionary
"""
Calculate the average score for each player and create a new dictionary
with player names as keys and their average scores as values.
"""
game_scores = {
    "Player1": {"scores": [45, 52, 48, 50]},
    "Player2": {"scores": [38, 42, 40, 45]},
    "Player3": {"scores": [55, 58, 60, 57]}
}

# Your solution here:

averages = {k: sum(v['scores'])/len(v["scores"]) for k,v in game_scores.items()}

print(averages)




# PROBLEM 7: Categorizing Based on Conditions
"""
Categorize employees as "High Performer" (rating >= 4.5), 
"Average" (rating >= 3.5), or "Needs Review" (rating < 3.5).
Return a dictionary with employee IDs and their categories.
"""
employees = {
    "E001": {"name": "John", "rating": 4.8},
    "E002": {"name": "Jane", "rating": 3.2},
    "E003": {"name": "Bob", "rating": 4.2}
}

# Your solution here

employee_categories = {
    k: (
        "High Performer" if v["rating"] >= 4.5
        else "Average" if v["rating"] >= 3.5
        else "Needs Review"
    )
    for k,v in employees.items()
}

print(employee_categories)



# PROBLEM 8: Lambda Functions - Sorting
"""
Use lambda functions to:
- Sort a list of tuples by the second element
- Filter items greater than 50
- Calculate squares of numbers
"""
data = [(1, 45), (2, 78), (3, 23), (4, 90)]
numbers = [5, 12, 8, 25, 3, 61, 18]

# Your solution here:

sorted_data = sorted(data, key=lambda x: x[1])            # //////////////////////////
filtered = list(filter(lambda x: x > 50, numbers))
squares = list(map(lambda x: x**2, numbers))

print(sorted_data, filtered, squares)




# PROBLEM 9: Finding Elements with Index
"""
Write a function that takes a list and a threshold value.
Return a list of tuples containing (index, value) for all values
that exceed the threshold.
"""
prices = [25, 48, 62, 35, 78, 42, 90, 15]

# Your solution here:

def find_above_threshold(lst, threshold):
    return [(i, v) for i,v in enumerate(lst) if v > threshold]

print(find_above_threshold(prices, 50))



# PROBLEM 10: Dictionary with Index in Nested Structure
"""
Given weather data, find all days and times (index) where 
humidity exceeded 70%. Return as list of tuples (day, time_index, value).
"""
humidity_data = {
    "Day1": [65, 72, 68, 75, 70],
    "Day2": [80, 78, 72, 69, 71],
    "Day3": [60, 65, 68, 64, 62]
}

# Your solution here

def above_70_humidity(humidity_dict):
    return [(k, i, h)
            for k,v in humidity_dict.items()
            for i,h in enumerate(v) if h > 70]

print(above_70_humidity(humidity_data))




# PROBLEM 11: Working with Zero Values
"""
Calculate total sales for each salesperson, but exclude days 
where sales were zero. Return a dictionary with name and total.
"""
sales_data = {
    "Tom": [1200, 0, 1500, 1800, 0, 1600],
    "Lisa": [1400, 1300, 0, 1700, 1500, 0],
    "Mark": [1100, 1200, 1300, 0, 1400, 1500]
}

# Your solution here

def getTotalSales(sales_data):
    return {k: sum([n for n in v if n != 0])
            for k,v in sales_data.items()}

print(getTotalSales(sales_data))


# PROBLEM 12: Conditional Dictionary Comprehension with Filter
"""
Create a dictionary containing only salespeople who achieved
total sales greater than 6000 (excluding zeros).
"""
# Use sales_data from Problem 11

# Your solution here:

top_performers = {k: [i for i in v if i != 0]
                  for k,v in sales_data.items()
                  if sum([i for i in v if i !=0])> 6000}

print(top_performers)



# PROBLEM 13: Complex Salary Calculation
"""
Calculate monthly salary based on rules:
- Base rate: 100 Tk per hour for standard hours (8)
- Reduced rate: 80 Tk per hour for less than 8
- Overtime: 150 Tk per hour beyond 8
Return dictionary with names and total salary.
"""
work_hours = {
    "Alex": [8, 7, 9, 8, 10],
    "Beth": [8, 8, 8, 7, 8],
    "Chris": [9, 10, 8, 9, 11]
}
# Your solution here

def getDaySalary(h):
    if h == 8: return 100*h
    elif h > 8: return 8*100 + (h-8)*150
    else: return 80*h

def getTotalSalary(work_hours):
    return {k: sum([getDaySalary(i) for i in v])
            for k,v in work_hours.items()}

print(getTotalSalary(work_hours))




# PROBLEM 14: Generator Function Basics
"""
Create a generator function that yields only even numbers
from a given list. Demonstrate iteration.
"""
nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Your solution here:

def even_generator(lst):
    for n in lst:
        if n % 2== 0:
            yield n
        
even_list = [n for n in even_generator(nums)]
print(even_list)



# PROBLEM 15: Generator vs Regular Function
"""
Compare memory usage:
- Create a regular function that returns a list of squares
- Create a generator that yields squares
Explain the difference and when to use each.
"""

# Your solution here

def reg_func():
    myList = [1, 2, 3, 4, 5]
    return [i**2 for i in myList]

def gen_func():
    myList = [1, 2, 3, 4, 5]
    for i in myList:
        yield i**2

print(reg_func())
# Use regular functions when the dataset is small
for i in gen_func(): print(i)
# Use generators when working with large data




# PROBLEM 16: Filtering with Average Calculation
"""
Calculate the average value of all items in a list.
Then create a generator that yields only items above average.
"""
values = [45, 78, 23, 89, 56, 34, 67, 90, 12, 88]

# Your solution here

def above_average(values):
    average = sum(values)/len(values)
    for i in values:
        if i > average:
            yield i
        
print([i for i in above_average(values)])




# PROBLEM 17: Generator for Dictionary Values
"""
Create a generator function that takes a list of dictionaries
and yields only those where a specific key's value exceeds
a threshold.
"""
items = [
    {"name": "Item1", "value": 120},
    {"name": "Item2", "value": 85},
    {"name": "Item3", "value": 150},
    {"name": "Item4", "value": 95}
]

# Your solution here

def getFunction(list_of_dict, threshold=100):
    for i in list_of_dict:
        if i["value"] > threshold:
            yield i

for i in getFunction(items): print(i)



# PROBLEM 18: Nested Dictionary Processing
"""
Given student test data, calculate each student's average
and return a new dictionary with student IDs as keys and
averages as values.
"""
test_results = {
    "ST01": {"name": "Anna", "marks": [88, 92, 85, 90]},
    "ST02": {"name": "Ben", "marks": [75, 78, 72, 80]},
    "ST03": {"name": "Cara", "marks": [95, 98, 92, 96]}
}

# Your solution here

def student_average_dict(test_result):
    return {k: sum(v["marks"])/len(v["marks"]) 
            for k,v in test_result.items()}

print(student_average_dict(test_results))



# PROBLEM 19: Multi-condition Filtering
"""
Write a function that processes transaction data and returns
a summary dictionary containing:
- Total revenue (sum of all positive values)
- Total expenses (sum of all negative values)
- Net profit (revenue - expenses)
- Number of profitable days (positive values)
"""
transactions = [1500, -800, 2200, -600, 1800, -400, 2500, -900]


# Your solution here

def process_transaction(t_list):
    revenue_list = [i for i in t_list if i >= 0]
    total_revenue = sum(revenue_list)
    total_expenses = sum([i for i in t_list if i < 0])
    net_profit = total_revenue + total_expenses
    return {
        "total_revenue": total_revenue,
        "total_expenses": total_expenses,
        "net_profit": net_profit,
        "profitable_days": len(revenue_list)
    }

print(process_transaction(transactions))




# PROBLEM 20: Complex Data Transformation
"""
Given sensor readings throughout a week:
1. Calculate average reading for each day
2. Find days where average exceeds 25
3. Return a list of tuples: (day, average, max_reading)
Use lambda functions and list comprehension where appropriate.
"""
sensor_data = {
    "Mon": [22, 24, 26, 25, 23],
    "Tue": [20, 21, 23, 22, 20],
    "Wed": [26, 28, 30, 29, 27],
    "Thu": [24, 26, 28, 27, 25],
    "Fri": [21, 23, 25, 24, 22]
}

# Your solution here

def process_sensor(sensor_data):
    avg = lambda x: sum(x)/len(x)
    return [(k, avg(v), max(v)) 
            for k,v in sensor_data.items() 
            if avg(v) > 25]
            
print(process_sensor(sensor_data))



