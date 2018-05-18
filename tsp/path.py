from random import shuffle
from typing import List

from tsp.city import City, EMPTY_CITY


class Path:
    def __init__(self, path):
        self.path = path if isinstance(path, List) else [EMPTY_CITY] * path
        self.fit = 0

    def shuffle(self):
        shuffle(self.path)
        return self

    def fitness(self):
        if self.fit == 0:
            self.fit = 1 / self.distance()
        return self.fit

    def distance(self):
        temp = len(self.path)
        dist = sum([self.path[i].distance(self.path[(i + 1) % temp]) for i in range(temp)])
        return dist

    def swap(self, from_index, to_index):
        self.path[from_index], self.path[to_index] = self.path[to_index], self.path[from_index]

    def add(self, other_path):
        empty_indices = [i for i in range(len(self.path)) if self.path[i] == EMPTY_CITY]
        if len(empty_indices) == 0:
            return
        current_empty = 0
        for city in other_path:
            if city not in self:
                self.path[empty_indices[current_empty]] = city
                current_empty += 1

    def __getitem__(self, item):
        return self.path[item]

    def __setitem__(self, key, value):
        self.path[key] = value

    def __contains__(self, item):
        return any(x == item for x in self.path)

    def __len__(self):
        return len(self.path)

    def __str__(self):
        return ",".join([str(p) for p in self.path])

    def __eq__(self, other):
        return self.path == other.path

    def __iter__(self):
        return iter(self.path)
