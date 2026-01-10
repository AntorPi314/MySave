# Group 4: Online Learning Platform Analytics System

# Design an analytics system for an online learning platform.
# Implement a base class User containing _user_id (int) and _name (str),
# along with method dashboard() and __str__().
# This class must demonstrate constructor usage, encapsulation, and polymorphism.


class User:
    def __init__(self, user_id, name):
        self._user_id = user_id
        self._name = name

    def dashboard(self):
        return f"Dashboard for {self._name}"

    def __str__(self):
        return f"UserID: {self._user_id}, Name: {self._name}"


# Create a class Student that inherits from User and contains _progress (dictionary)
# and _scores (dictionary).
# Implement methods add_scores(course_id, *scores),
# calculate_completion(course_id), and a @property to access completion percentage.
# This class must demonstrate inheritance, property decorator, args usage,
# loops, conditional logic, and exception handling.


class Student(User):
    def __init__(self, user_id, name):
        super().__init__(user_id, name)
        self._progress = {}
        self._scores = {}

    def add_scores(self, course_id, *scores):
        try:
            if course_id not in self._scores:
                self._scores[course_id] = []
            for s in scores:
                self._scores[course_id].append(s)
        except Exception as e:
            print("Error adding scores:", e)

    def calculate_completion(self, course_id):
        try:
            if course_id not in self._progress:
                self._progress[course_id] = 0
            completed = len(self._scores.get(course_id, []))
            self._progress[course_id] = min(completed * 20, 100)
            return self._progress[course_id]
        except Exception as e:
            return str(e)

    @property
    def completion_percentage(self):
        if not self._progress:
            return 0
        return sum(self._progress.values()) / len(self._progress)


# Create a class Instructor that inherits from User and contains courses_taught (set).
# Implement method view_course_analytics(course_id).
# This class must demonstrate set operations, inheritance,
# and formatted string output.


class Instructor(User):
    def __init__(self, user_id, name):
        super().__init__(user_id, name)
        self.courses_taught = set()

    def add_course(self, course_id):
        self.courses_taught.add(course_id)

    def view_course_analytics(self, course_id):
        if course_id in self.courses_taught:
            return f"Instructor {self._name} viewing analytics for Course {course_id}"
        return "Course not assigned to instructor"


# Create classes Course and LearningPlatform, where Course contains
# course_id, title, and total_marks, and LearningPlatform manages users and courses.
# Implement methods load_users_from_dict(), student_stream(),
# sort_students(key_name), and generate_certificate().
# The platform must use generators, lambda expressions,
# map/filter/reduce, sorting with custom key,
# exception handling, and string formatting.


from functools import reduce


class Course:
    def __init__(self, course_id, title, total_marks):
        self.course_id = course_id
        self.title = title
        self.total_marks = total_marks

    def __str__(self):
        return f"CourseID: {self.course_id}, Title: {self.title}, Marks: {self.total_marks}"


class LearningPlatform:
    def __init__(self):
        self.users = []
        self.courses = {}

    def load_users_from_dict(self, data_list):
        for data in data_list:
            if data["type"] == "student":
                self.users.append(Student(data["user_id"], data["name"]))
            elif data["type"] == "instructor":
                self.users.append(Instructor(data["user_id"], data["name"]))

    def add_course(self, course):
        self.courses[course.course_id] = course

    def student_stream(self):
        for u in self.users:
            if isinstance(u, Student):
                yield u

    def sort_students(self, key_name):
        try:
            students = list(self.student_stream())
            return sorted(students, key=lambda s: getattr(s, key_name))
        except Exception as e:
            return str(e)

    def generate_certificate(self, student, course_id):
        completion = student.calculate_completion(course_id)
        if completion >= 100:
            return f"Certificate awarded to {student._name} for Course {course_id}"
        return f"{student._name} has not completed Course {course_id}"

    def average_completion(self):
        try:
            students = list(self.student_stream())
            return reduce(
                lambda t, s: t + s.completion_percentage,
                students,
                0
            ) / len(students)
        except Exception as e:
            return str(e)


# =========================
# Example Usage
# =========================

platform = LearningPlatform()

platform.load_users_from_dict([
    {"type": "student", "user_id": 1, "name": "Antor"},
    {"type": "student", "user_id": 2, "name": "Rahim"},
    {"type": "instructor", "user_id": 3, "name": "Karim"}
])

course1 = Course(101, "Python Basics", 100)
platform.add_course(course1)

students = list(platform.student_stream())

students[0].add_scores(101, 10, 15, 20, 25, 30)
students[1].add_scores(101, 20, 20)

print(students[0])
print("Completion:", students[0].calculate_completion(101))
print("Certificate:", platform.generate_certificate(students[0], 101))

print("\n--- Students Stream ---")
for s in platform.student_stream():
    print(s._name, "Completion:", s.completion_percentage)

print("\nAverage Completion:", platform.average_completion())






