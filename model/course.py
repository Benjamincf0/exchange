from model.uni import University
from model.schedule import CourseSchedule


class Course:
    def __init__(self, code, title, schedule: CourseSchedule, university: University, prerequisites: list['Course'] = []):
        self.code = code
        self.title = title
        self.schedule = schedule
        self.university = university
        self.prerequisites = prerequisites

    def __repr__(self):
        return f"Course({self.code}, {self.title}, {self.schedule}"