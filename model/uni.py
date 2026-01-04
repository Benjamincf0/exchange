class University:
    def __init__(self, name, location):
        self.name = name
        self.location = location

    def __str__(self):
        return f"University({self.name}, {self.location})"