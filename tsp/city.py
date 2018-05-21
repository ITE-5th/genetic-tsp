import math


class City:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, other_city):
        return math.hypot(self.x - other_city.x, self.y - other_city.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __getitem__(self, item):
        return self.x if item == 0 else self.y

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        else:
            self.y = value

    def __str__(self):
        return f"x = {self.x}, y = {self.y}"


EMPTY_CITY = City(None, None)
