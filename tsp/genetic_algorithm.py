from random import random

import numpy as np

from tsp.path import Path
from tsp.population import Population


class GeneticAlgorithm:
    def __init__(self, cities, population_size=10, mutation_rate=0.015, tournament_size=5):
        self.population = Population.create_initial_population(cities, population_size)
        self.mutation_rate = mutation_rate
        self.tournament_size = tournament_size

    def evolve_for(self, iterations=100):
        pop = self.population
        fittest = pop.fittest()
        for i in range(iterations):
            pop = self.evolve(pop)
            temp = pop.fittest()
            if temp.fitness() > fittest.fitness():
                fittest = temp
        return fittest

    def evolve(self, population: Population):
        pop = Population([])
        temp = len(population)
        for i in range(temp):
            first, second = self.select(population), self.select(population)
            child = self.cross_over(first, second)
            self.mutate(child)
            pop.add(child)
        return pop

    @staticmethod
    def cross_over(first: Path, second: Path):
        temp = len(first)
        child = Path(temp)
        from_index, to_index = int(random() * temp), int(random() * temp)
        from_index, to_index = min(from_index, to_index), max(from_index, to_index)
        child[from_index:to_index] = first[from_index:to_index]
        child.add(second)
        return child

    def mutate(self, path: Path):
        temp = len(path)
        rn = np.random.binomial(size=temp, p=self.mutation_rate, n=1)
        for r in rn:
            if r == 1:
                from_index, to_index = int(random() * temp), int(random() * temp)
                path.swap(from_index, to_index)

    def select(self, population: Population):
        pop = Population([])
        temp = len(population)
        for i in range(self.tournament_size):
            pop.add(population[int(random() * temp)])
        return pop.fittest()
