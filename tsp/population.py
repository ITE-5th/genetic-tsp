from tsp.path import Path


class Population:

    def __init__(self, paths):
        self.paths = paths

    @staticmethod
    def create_initial_population(cities, population_size):
        return Population([Path(cities).shuffle() for _ in range(population_size)])

    def fittest(self):
        best_path = self.paths[0]
        for i in range(1, len(self.paths)):
            if self.paths[i].fitness() > best_path.fitness():
                best_path = self.paths[i]
        return best_path

    def add(self, path):
        self.paths.append(path)

    def __len__(self):
        return len(self.paths)

    def __getitem__(self, item):
        return self.paths[item]

    def __setitem__(self, key, value):
        self.paths[key] = value

    def __str__(self):
        return "\n".join(str(i) for i in self.paths)
