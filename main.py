from tsp.city import City
from tsp.genetic_algorithm import GeneticAlgorithm

if __name__ == '__main__':
    iterations = 100
    population_size = 10
    mutation_rate = 0.15
    tournament_size = 5
    cities = [City(1, 2), City(4, 5), City(6, 7), City(10, 12), City(15, 18)]
    ga = GeneticAlgorithm(cities, population_size, mutation_rate, tournament_size)
    solution = ga.evolve_for(iterations)
    print(f"solution = {solution}\ndistance = {1 / solution.fitness()}")
