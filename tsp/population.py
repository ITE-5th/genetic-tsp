from tsp.city import City
from tsp.path import Path


class Population:

    def __init__(self, paths):
        self.paths = paths

    @staticmethod
    def create_initial_population(cities, population_size):
        pop = Population([])
        for i in range(population_size):
            path = Path(cities)
            path.shuffle()
            pop.add(path)
        return pop

    def fittest(self):
        best_path = self.paths[0]
        for i in range(1, len(self.paths)):
            if self.paths[i].fitness() > best_path.fitness():
                best_path = self.paths[i]
        return best_path

    def add(self, path):
        self.paths.append(path)

    def population_sizes(self):
        return ",".join([str(len(path)) for path in self.paths])

    def __len__(self):
        return len(self.paths)

    def __getitem__(self, item):
        return self.paths[item]

    def __setitem__(self, key, value):
        self.paths[key] = value

    def __iter__(self):
        return iter(self.paths)

    def __str__(self):
        return "\n".join(str(i) for i in self.paths)


if __name__ == '__main__':
    cities = [City(1, 1), City(1, 2), City(2, 2), City(3, 2)]
    print(Population.create_initial_population(cities, 5))
