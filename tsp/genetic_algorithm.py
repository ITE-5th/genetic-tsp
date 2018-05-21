from random import random

import numpy as np

from tsp.path import Path
from tsp.population import Population


class GeneticAlgorithm:
    def __init__(self, cities, population_size=10, mutation_rate=0.015, tournament_size=5):
        self.population = Population.create_initial_population(cities, population_size)
        self.mutation_rate = mutation_rate
        self.tournament_size = tournament_size

    def evolve(self, iterations=100):
        pop = self.population
        fittest = pop.fittest()
        for i in range(iterations):
            pop = self.evolve_once(pop)
            temp = pop.fittest()
            if temp.fitness() > fittest.fitness():
                fittest = temp
        return fittest

    def evolve_once(self, population: Population):
        pop = Population([])
        temp = len(population)
        for i in range(temp):
            first, second = self.select(population), self.select(population)
            child = self.cross_over(first, second)
            child = self.mutate_once(child)
            pop.add(child)
        return pop

    @staticmethod
    def cross_over(first: Path, second: Path):
        temp = len(first)
        child = Path(temp)
        from_index, to_index = int(random() * temp), int(random() * temp)
        from_index, to_index = min(from_index, to_index), max(from_index, to_index)
        child[from_index:to_index] = first[from_index:to_index]
        child.add_path(second)
        return child

    def mutate_once(self, path: Path):
        temp = len(path)
        rn = np.random.binomial(size=1, p=self.mutation_rate, n=1)[0]
        if rn == 1:
            from_index, to_index = int(random() * temp), int(random() * temp)
            path.swap(from_index, to_index)
        return path

    def mutate(self, path: Path):
        for _ in range(len(path)):
            path = self.mutate_once(path)
        return path

    def select(self, population: Population):
        pop = Population([])
        temp = len(population)
        for i in range(self.tournament_size):
            pop.add(population[int(random() * temp)])
        return pop.fittest()
