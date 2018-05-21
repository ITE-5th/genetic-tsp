from tsp.city import City
from tsp.genetic_algorithm import GeneticAlgorithm

if __name__ == '__main__':
    population_size = 10
    mutation_rate = 0.015
    tournament_size = 10
    iterations = 1000
    cities = [City(0, 0), City(20, 0), City(0, 20), City(20, 20)]
    ga = GeneticAlgorithm(cities, population_size=population_size, mutation_rate=mutation_rate,
                          tournament_size=tournament_size)
    solution = ga.evolve(iterations)
    print(f"path : {solution}")
