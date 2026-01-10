# Group 1: University Academic Management System

# Design a program to manage a university academic system.
# Implement an abstract class Person that contains attributes _id (int), _name (str), and _email (str).
# It must define an abstract method get_role() and a concrete method __str__() for formatted output.
# The class must demonstrate abstract base class usage,
# constructor usage, encapsulation, and string formatting.


from abc import ABC, abstractmethod
from functools import reduce


class Person(ABC):
    def __init__(self, id: int, name: str, email: str):
        self._id = id
        self._name = name
        self._email = email

    @abstractmethod
    def get_role(self):
        pass

    def __str__(self):
        return f"ID: {self._id}, Name: {self._name}, Email: {self._email}, Role: {self.get_role()}"


# Create a class Student that inherits from Person and contains attributes
# _enrolled_courses (list), _marks (dictionary), and _cgpa (float).
# Implement methods enroll(*course_codes), add_marks(**course_marks), and calculate_cgpa().
# Use a @property for accessing CGPA and prevent direct modification.
# This class must implement inheritance, encapsulation, polymorphism,
# property decorator, loops, conditional logic, dictionary operations,
# and exception handling.


class Student(Person):
    def __init__(self, id, name, email):
        super().__init__(id, name, email)
        self._enrolled_courses = [] 
        self._marks = {}
        self._cgpa = 0.0

    def get_role(self):
        return "Student"

    def enroll(self, *course_codes):
        for c in course_codes:
            if c not in self._enrolled_courses:
                self._enrolled_courses.append(c)

    def add_marks(self, **course_marks):
        try:
            for course, mark in course_marks.items():
                if course not in self._enrolled_courses:
                    raise Exception("Student not enrolled in course")
                self._marks[course] = mark
        except Exception as e:
            print("Error:", e)

    def calculate_cgpa(self):
        if not self._marks:
            self._cgpa = 0.0
        else:
            avg = sum(self._marks.values()) / len(self._marks)
            self._cgpa = round(avg / 25, 2)
        return self._cgpa

    @property
    def cgpa(self):
        return self._cgpa


# Create a class Instructor that inherits from Person and contains
# _assigned_courses (set) and _salary (float).
# Implement methods assign_course(course_code) and
# evaluate_student(student, course_code, marks).
# Use a static method validate_salary(value) and a class method from_dict(data).
# This class must implement inheritance, static method, class method,
# set usage, and validation logic.


class Instructor(Person):
    def __init__(self, id, name, email, salary):
        if not Instructor.validate_salary(salary):
            raise ValueError("Invalid salary")
        super().__init__(id, name, email)
        self._assigned_courses = set()
        self._salary = salary

    def get_role(self):
        return "Instructor"

    def assign_course(self, course_code):
        self._assigned_courses.add(course_code)

    def evaluate_student(self, student, course_code, marks):
        if course_code in self._assigned_courses:
            student.add_marks(**{course_code: marks})

    @staticmethod
    def validate_salary(value):
        return value > 0

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["id"],
            data["name"],
            data["email"],
            data["salary"]
        )


# Create a class UniversitySystem containing attributes
# students (list), instructors (list), and courses (dictionary).
# Implement methods add_student(), add_instructor(),
# load_students_from_dict(), student_generator(),
# and sort_students(key_name).
# The class must use generators, sorting with custom key,
# lambda, map/filter/reduce, loops, exception handling,
# and control execution through a menu-driven loop.


class UniversitySystem:
    def __init__(self):
        self.students = []
        self.instructors = []
        self.courses = {}

    def add_student(self, student):
        self.students.append(student)

    def add_instructor(self, instructor):
        self.instructors.append(instructor)

    def load_students_from_dict(self, data_list):
        for d in data_list:
            self.add_student(Student(d["id"], d["name"], d["email"]))

    def student_generator(self):
        for s in self.students:
            yield s

    def sort_students(self, key_name):
        try:
            return sorted(self.students, key=lambda s: getattr(s, key_name))
        except Exception as e:
            print("Sorting Error:", e)

    def average_cgpa(self):
        try:
            return reduce(lambda t, s: t + s.cgpa, self.students, 0) / len(self.students)
        except Exception as e:
            return str(e)


# =========================
# Example Usage
# =========================

uni = UniversitySystem()

uni.load_students_from_dict([
    {"id": 1, "name": "Antor", "email": "antor@mail.com"},
    {"id": 2, "name": "Rahim", "email": "rahim@mail.com"}
])

inst = Instructor.from_dict({
    "id": 101,
    "name": "Dr. Karim",
    "email": "karim@mail.com",
    "salary": 60000
})

uni.add_instructor(inst)

inst.assign_course("CSE101")
inst.assign_course("CSE102")

s1, s2 = uni.students

s1.enroll("CSE101", "CSE102")
s2.enroll("CSE101")

inst.evaluate_student(s1, "CSE101", 80)
inst.evaluate_student(s1, "CSE102", 85)
inst.evaluate_student(s2, "CSE101", 70)

s1.calculate_cgpa()
s2.calculate_cgpa()

print("---- Students ----")
for s in uni.student_generator():
    print(s, "CGPA:", s.cgpa)

print("\nAverage CGPA:", uni.average_cgpa())




