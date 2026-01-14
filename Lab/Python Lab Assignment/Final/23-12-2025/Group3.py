
# Group 3: Employee Performance and Payroll System

# Design a system to analyze employee performance. Implement an abstract class Employee containing _emp_id (int), _name (str), 
# _base_salary (float), and _performance_scores (list). Declare an abstract method calculate_bonus() and implement __str__(). 
# This class must demonstrate abstract base class, encapsulation, constructor usage, and formatted output.


from abc import ABC, abstractmethod
from functools import reduce

# =========================
# Abstract Base Class
# =========================
class Employee(ABC):
    def __init__(self, emp_id, name, base_salary):
        self._emp_id = emp_id
        self._name = name
        self._base_salary = base_salary
        self._performance_scores = []

    # -------- property & setter --------
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        self._name = value

    @property
    def salary(self):
        return self._base_salary

    @salary.setter
    def salary(self, value):
        if value <= 0:
            raise ValueError("Salary must be positive")
        self._base_salary = value

    # -------- common method --------
    def add_scores(self, scores):
        for s in scores:
            self._performance_scores.append(s)

    @abstractmethod
    def calculate_bonus(self):
        pass

    def __str__(self):
        return (
            f"ID: {self._emp_id}, "
            f"Name: {self._name}, "
            f"Salary: {self._base_salary}, "
            f"Scores: {self._performance_scores}"
        )



# Create a class Developer that inherits from Employee and contains programming_languages (list). 
# Implement calculate_bonus() using average performance score and use a @property for salary calculation. 
# This class must demonstrate inheritance, polymorphism, property decorator, list operations, and conditional logic.


# =========================
# Developer Class
# =========================
class Developer(Employee):
    def __init__(self, emp_id, name, base_salary, programming_languages):
        super().__init__(emp_id, name, base_salary)
        self.programming_languages = programming_languages

    def calculate_bonus(self):
        if not self._performance_scores:
            return 0
        avg_score = sum(self._performance_scores) / len(self._performance_scores)

        if avg_score >= 8:
            return self.salary * 0.20
        elif avg_score >= 5:
            return self.salary * 0.10
        else:
            return self.salary * 0.05


# Create a class Manager that inherits from Employee and contains team_size (int).
# Override calculate_bonus() with a different logic. Use a static method validate_score(score) and a class method from_dict(data).
# This class must demonstrate method overriding, static method, class method, and validation logic.


# =========================
# Manager Class
# =========================
class Manager(Employee):
    def __init__(self, emp_id, name, base_salary, team_size):
        super().__init__(emp_id, name, base_salary)
        self.team_size = team_size

    def calculate_bonus(self):
        if not self._performance_scores:
            return 0
        avg = sum(self._performance_scores) / len(self._performance_scores)
        return (self.salary * 0.15) + (self.team_size * avg * 100)

    @staticmethod
    def validate_score(score):
        return 0 <= score <= 10

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["emp_id"],
            data["name"],
            data["base_salary"],
            data["team_size"]
        )


# Create a controller class CompanySystem containing employees (dictionary). 
# Implement methods add_employee(), add_performance_scores(scores), high_performer_generator(), total_payroll(), and sort_employees(key_name).
# The class must use loops, generators, lambda expressions, map/filter/reduce, sorting with custom key, and exception handling.


# =========================
# Controller Class
# =========================
class CompanySystem:
    def __init__(self):
        self.employees = {}

    def add_employee(self, employee):
        self.employees[employee._emp_id] = employee

    def add_performance_scores(self, emp_id, scores):
        try:
            valid_scores = list(
                filter(Manager.validate_score, scores)
            )
            self.employees[emp_id].add_scores(valid_scores)
        except KeyError:
            print("Employee not found")

    def high_performer_generator(self, threshold=8):
        for e in self.employees.values():
            if e._performance_scores:
                avg = sum(e._performance_scores) / len(e._performance_scores)
                if avg >= threshold:
                    yield e

    def total_payroll(self):
        try:
            return reduce(
                lambda total, e: total + e.salary + e.calculate_bonus(),
                self.employees.values(),
                0
            )
        except Exception as e:
            print("Error calculating payroll:", e)

    def sort_employees(self, key_name):
        return sorted(
            self.employees.values(),
            key=lambda e: getattr(e, key_name)
        )
    


# =========================
# Example Usage
# =========================
company = CompanySystem()

dev = Developer(1, "Antor", 50000, ["Python", "Java"])
mgr = Manager.from_dict({
    "emp_id": 2,
    "name": "Rahim",
    "base_salary": 70000,
    "team_size": 5
})

company.add_employee(dev)
company.add_employee(mgr)

company.add_performance_scores(1, [8, 9, 7])
company.add_performance_scores(2, [9, 8, 10])

print("---- Employees ----")
for e in [company.sort_employees("name")]:
    print(e)
    print("Bonus:", e.calculate_bonus())

print("\n---- High Performers ----")
for hp in company.high_performer_generator():
    print(hp.name)

print("\nTotal Payroll:", company.total_payroll())

