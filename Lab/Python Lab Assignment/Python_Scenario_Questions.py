# Question 1: Employee Bonus Calculator
"""
 Scenario: Your company needs a system to calculate employee bonuses based on performance
 ratings and years of service.
 Write a function calculate_team_bonuses(employees) that takes a list of employee
 dictionaries and returns a dictionary with employee names as keys and their bonus amounts as values.

 Rules:
 ● Base bonus is $1000
 ● If performance rating >= 4, multiply bonus by 1.5
 ● If years of service > 5, add $500 extra
 ● Use list comprehension to filter employees with rating >= 3
 ● Only employees with rating >= 3 are eligible for bonuses
"""
employees = [
{'name': 'Alice', 'rating': 4.5, 'years': 6},
{'name': 'Bob', 'rating': 3.2, 'years': 3},
{'name': 'Charlie', 'rating': 2.8, 'years': 4},
{'name': 'Diana', 'rating': 4.8, 'years': 7}
]

def calculateBonus(rating, years):
    bonus = 1000
    if rating >= 4: bonus = bonus*1.5
    if years > 5: bonus = bonus + 500
    return bonus


def calculate_team_bonuses(employees):
    eligible_employees = [i for i in employees if i["rating"] >= 3]
    return {i["name"]: calculateBonus(i["rating"], i["years"])
            for i in eligible_employees
    }

# print(calculate_team_bonuses(employees))



# Question 2: Prime Number Generator with Filtering
"""
 Scenario: Create a system that generates prime numbers and filters them based on conditions.
 Write a generator function prime_generator(start, end) that yields prime numbers
 in a range. Then create a function get_filtered_primes(start, end,condition) that uses the generator
 and list comprehension to return primes meeting a specific condition.

 Requirements:
 ● Use a generator function for memory efficiency
 ● Use a nested loop to check if a number is prime
 ● Use list comprehension to apply the condition function
 ● The condition function should be passed as a parameter

# Get all primes between 10-50 that are greater than 20
result = get_filtered_primes(10, 50, lambda x: x > 20)
# Should return: [23, 29, 31, 37, 41, 43, 47]
"""
def prime_generator(start, end):
        for n in range(start, end):
            if n > 1:
                for i in range(2, int(n**0.5)+1):
                    if n%i == 0: break
                else: yield n

def get_filtered_primes(start, end, condition):
    return [p for p in prime_generator(start, end) if condition(p)]

# print(get_filtered_primes(1, 50, lambda x: x>20))



# Question 3: Shopping Cart with Dynamic Discounts
"""
 Scenario: Build a shopping cart system with conditional discount rules.
 Create a function apply_discounts(cart_items, discount_rules) that
 processes cart items and applies multiple discount rules based on conditions.

 Rules to implement using loops and conditions:
 ● If quantity > 5, apply 10% discount on that item
 ● If total price > $100, apply additional 5% on entire cart
 ● Use dictionary comprehension to create the final price dictionary
 ● Use a generator expression to calculate the total efficiently

Expected Output Format:
{
    'laptop': 760.0,  # 5% off total cart discount
    'mouse': 142.5,   # 10% off quantity + 5% off total
    'keyboard': 142.5  # 5% off total cart discount
}
"""
cart_items = {
'laptop': {'price': 800, 'quantity': 1},
'mouse': {'price': 25, 'quantity': 6},
'keyboard': {'price': 50, 'quantity': 3}
}

def cal_discount(price, quantity, totalPrice):
     final_price = price*quantity
     if quantity > 5: final_price -= price*quantity*0.10
     if totalPrice > 100: final_price -= price*quantity*0.05
     return final_price

def discount_rules(cart_items):
     total_price = sum([i['price']*i['quantity'] for i in cart_items.values()])
     for k, v in cart_items.items():
          yield k, cal_discount(v['price'], v['quantity'], total_price)
     
     
def apply_discounts(cart_items, discount_rules):
     return {k: v for k,v in discount_rules(cart_items)}
          

# print(apply_discounts(cart_items, discount_rules))



# Question 4: Student Grade Analyzer
"""
 Scenario: Create a comprehensive grade analysis system for a class.
 Write a function analyze_grades(students) that processes student data and generates multiple reports.

 Requirements:
 ● Use a generator function grade_generator(students) that yields one student's average at a time
 ● Use list comprehension to categorize students: 'Excelent' (avg>=90), 'Good' (avg>=75), 'Pass' (avg>=60), 'Fail' (avg<60)
 ● Use dictionary comprehension to create a grade distribution count
 ● Use nested loops to find the top 3 students
 ● Use conditional expressions within comprehensions
"""
students = [
{'name': 'Alex', 'scores': [85, 90, 78, 92]},
{'name': 'Beth', 'scores': [92, 95, 88, 91]},
{'name': 'Carl', 'scores': [65, 70, 68, 72]},
{'name': 'Dana', 'scores': [55, 60, 58, 62]}
]

def grade_generator(students):
     for i in students:
          yield sum(i['scores'])/len(i['scores']), i['name']

def get_grade_distribution(avg):
     if avg >= 90: return 'Excellent'
     elif avg >= 75: return 'Good'
     elif avg >= 60: return 'Pass'
     else: return 'Fail'

def analyze_grades(students):
     categories = ['Excellent', 'Good', 'Pass', 'Fail']
     categorized_students = {c: [name for avg,name in grade_generator(students) 
                                 if get_grade_distribution(avg) == c] 
                             for c in categories}
     
     top_performers = [(x['name'], sum(x['scores'])) for x in students]
     top_performers = sorted(top_performers, key=lambda x: x[1], reverse=True)
     top_performers = [x[0] for x in top_performers[:3]]
     return {
          "categorized_students": categorized_students,
          "grade_distribution": {k: len(v) for k,v in categorized_students.items()},
          "top_performers": top_performers
     }
print(analyze_grades(students))
     







import string

# -------------------------
# Generator: Suggest improvements
# -------------------------
def password_suggestion_generator(password):
    suggestions = [
        ("length", "Increase length (min 8 chars)", lambda p: len(p) >= 8),
        ("uppercase", "Add uppercase letter", lambda p: any(c.isupper() for c in p)),
        ("lowercase", "Add lowercase letter", lambda p: any(c.islower() for c in p)),
        ("digit", "Add digit", lambda p: any(c.isdigit() for c in p)),
        ("special", "Add special characters", lambda p: any(c in string.punctuation for c in p))
    ]

    for label, suggestion, check in suggestions:
        if not check(password):
            yield suggestion   # generator yields one suggestion at a time


# -------------------------
# Validator + Suggestor
# -------------------------
def validate_and_suggest_passwords(passwords):

    def count_criteria(p):
        return sum([
            len(p) >= 8,
            any(c.isupper() for c in p),
            any(c.islower() for c in p),
            any(c.isdigit() for c in p),
            any(c in string.punctuation for c in p)
        ])

    result = {
        pwd: {
            "strength": (
                "Strong" if (c := count_criteria(pwd)) == 5 
                else "Medium" if 3 <= c < 5 
                else "Weak"
            ),
            "suggestions": [s for s in password_suggestion_generator(pwd)]
        }
        for pwd in passwords
    }

    return result


# -------------------------
# Example Input
# -------------------------
passwords = ['Pass123!', 'weak', 'SuperSecure#2024', 'hello123']
print(validate_and_suggest_passwords(passwords))







