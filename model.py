


class Course:
    def __init__(self, code, title, instructor, schedule, location, status, message):
        self.code = code
        self.title = title
        self.instructor = instructor
        self.schedule = schedule
        self.location = location
        self.status = status
        self.message = message

    def __repr__(self):
        return f"Course({self.code}, {self.title}, {self.instructor}, {self.schedule}, {self.location}, {self.status}, {self.message})"