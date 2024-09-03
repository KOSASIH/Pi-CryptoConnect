import numpy as np
from .ga_evolver import GaEvolver

class GaTrainer:
    def __init__(self, population_size, individual_size, mutation_rate, crossover_rate, generations):
        self.ga_evolver = GaEvolver(population_size, individual_size, mutation_rate, crossover_rate, generations)

    def train(self):
        population, log, hof = self.ga_evolver.evolve()
        return population, log, hof

    def get_best_individual(self, population):
        return max(population, key=lambda x: x.fitness.values[0])

    def get_best_fitness(self, population):
        return self.get_best_individual(population).fitness.values[0]
