from datetime import datetime

class Period:
    def __inti__(self, start: datetime, end: datetime):
        self.start = start
        self.end = end

class CourseSchedule:
    def __init__(self, periods: list[Period], repeats: str = "Weekly"):
        self.periods = periods

    def __str__(self):
        days_str = ', '.join(self.days)
        return f"Schedule({days_str} {self.start_time}-{self.end_time} at {self.location})"