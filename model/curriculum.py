from model.course import Course
from model.uni import University

class Curriculum:
    def __init__(self, base_uni: University, exchange_uni: University):
        self.base_uni = base_uni
        self.exchange_uni = exchange_uni
        self.courses: list[Course] = []

    def add_course(self, course: Course):
        self.courses.append(course)

    def __repr__(self):
        return f"Curriculum({self.base_uni}, Courses: {len(self.courses)})"