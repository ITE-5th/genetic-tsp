from misc.cities_reader import CitiesReader
from tsp.genetic_algorithm import GeneticAlgorithm

if __name__ == '__main__':
    iterations = 1000
    population_size = 100
    mutation_rate = 0.03
    tournament_size = 10
    cities = CitiesReader.read("data/usa_cities.txt")
    ga = GeneticAlgorithm(cities, population_size, mutation_rate, tournament_size)
    solution = ga.evolve_for(iterations)
    print(f"solution = {solution}\ndistance = {1 / solution.fitness()}")
