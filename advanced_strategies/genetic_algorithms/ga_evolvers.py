import numpy as np
import random
from deap import base, creator, tools, algorithms

class GaEvolver:
    def __init__(self, population_size, individual_size, mutation_rate, crossover_rate, generations):
        self.population_size = population_size
        self.individual_size = individual_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.generations = generations
        self.creator = creator
        self.toolbox = base.Toolbox()

    def create_individual(self):
        return [random.random() for _ in range(self.individual_size)]

    def create_population(self):
        return [self.create_individual() for _ in range(self.population_size)]

    def evaluate_individual(self, individual):
        # TO DO: implement fitness function
        return sum(individual),

    def register_functions(self):
        self.creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        self.creator.create("Individual", list, fitness=self.creator.FitnessMax)
        self.toolbox.register("attr_float", random.random)
        self.toolbox.register("individual", tools.initRepeat, self.creator.Individual, self.toolbox.attr_float, n=self.individual_size)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        self.toolbox.register("evaluate", self.evaluate_individual)
        self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.1)
        self.toolbox.register("select", tools.selTournament, tournsize=3)

    def evolve(self):
        self.register_functions()
        population = self.toolbox.population(n=self.population_size)
        hof = tools.HallOfFame(1)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", np.mean)
        stats.register("std", np.std)
        stats.register("min", np.min)
        stats.register("max", np.max)
        population, log = algorithms.eaSimple(population, self.toolbox, cxpb=self.crossover_rate, mutpb=self.mutation_rate, ngen=self.generations, stats=stats, halloffame=hof, verbose=True)
        return population, log, hof
