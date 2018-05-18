from tsp.city import City
from tsp.genetic_algorithm import GeneticAlgorithm

if __name__ == '__main__':
    iterations = 100
    population_size = 10
    mutation_rate = 0.15
    tournament_size = 5
    cities = [City(1, 2), City(4, 5), City(6, 7)]
    ga = GeneticAlgorithm(cities, population_size, mutation_rate, tournament_size)
    solution = ga.evolve_for(iterations)
    print(solution)
