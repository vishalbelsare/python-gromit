# Gromit: A simple pure-python evoluationary algorithm

import copy
import math
import random


class Gromit():

    def __init__(self, schema, fitness_handler, population_size=30, copy_weight=1, mutate_weight=1,
                 crossover_weight=1, kill_percent=.1, new_individual_handler=None):
        """Create a new Gromit evolver.

        Keywork arguments:
        schema -- A list of field names each individual's dict will have
        fitness_handler -- A callback that returns a fitness value based on an individual
        population_size -- The number of individuals to maintain for each generation
        copy_weight, mutate_weight, crossover_weight -- Relative weighting to determine the percentage
            of the new population is created from each operator (default is 1 for each, so each get 33.33%)
        kill_percent -- Percent of the weakest individuals to kill off each generation (default is .1, meaning 10%)
        new_individual_handler -- Handler to be called every time a new individual is created
        """
        self.schema = schema

        self.fitness_handler = fitness_handler
        self.new_individual_handler = new_individual_handler

        self.population_size = population_size

        self.copy_weight = copy_weight
        self.mutate_weight = mutate_weight
        self.crossover_weight = crossover_weight

        self.kill_percent = kill_percent

        # A list of the current individuals, always stored sorted by highest fitness
        self.current_population = None


    ################################################################################
    # Interface
    ################################################################################

    def set_new_individual_handler(self, handler):
        """Define a handler to be called for every new individual."""
        self.new_individual_handler = handler


    def evolve(self):
        """Create a new population by applying the operators to the current population and return the highest fitness value."""
        if not self.current_population:
            self.current_population = self.create_random_population()
            self.fitness_test_population()
            return self.current_population[0]['_fitness']

        old_population = self.current_population

        num_to_kill = math.floor(self.kill_percent * self.population_size)
        old_population = old_population[:num_to_kill * -1]
        old_population_length = len(old_population)

        weighted_total = self.mutate_weight + self.copy_weight + self.crossover_weight
        num_to_copy = math.floor((self.copy_weight / weighted_total) * old_population_length)
        num_to_mutate = math.floor((self.mutate_weight / weighted_total) * old_population_length)
        num_to_crossover = math.floor((self.crossover_weight / weighted_total) * old_population_length)

        # Copy the strongest individuals
        new_population = old_population[0:num_to_copy]

        # Mutate random individuals
        for i in range(0, num_to_mutate):
            new_population.append(self.mutate_individual(
                self.get_random_individual(old_population)
            ))

        # Crossover random individuals
        for i in range(0, num_to_crossover):
            individual1 = self.get_random_individual(old_population)
            individual2 = self.get_random_individual(old_population)

            new_population.append(self.crossover_individuals(individual1, individual2))

        # Create new random individuals
        while len(new_population) < self.population_size:
            new_population.append(self.get_new_individual())

        self.current_population = new_population
        self.fitness_test_population()

        return self.current_population[0]['_fitness']


    def get_current_population(self):
        """Return the current population."""
        return self.current_population


    def get_most_fit_individual(self):
        """Return the most fit individual."""
        if self.current_population:
            return self.current_population[0]
        else:
            return None


    ################################################################################
    # Evolution Helpers
    ################################################################################

    def clone_individual(self, old_individual):
        """Return a cloned individual without hidden fields."""
        new_individual = copy.copy(old_individual)

        for field in old_individual.keys():
            if field.startswith('_'):
                del new_individual[field]

        return new_individual


    def get_random_individual(self, population):
        """Return a random individual from a sorted population, weighting towards those with higher fitness."""
        return population[math.floor(random.random() ** 3 * len(population))]


    def get_new_individual(self):
        """Return a new randomized individual."""
        individual = {}

        for field in self.schema:
            if not field.startswith('_'):
                individual[field] = random.random()

        if self.new_individual_handler:
            self.new_individual_handler(individual)

        return individual


    def fitness_test_population(self):
        """Set '_fitness' for all individuals and sort the population by fitness."""
        population = self.current_population

        for individual in population:
            individual.pop('_fitness', None)
            individual['_fitness'] = self.fitness_handler(individual)

        self.current_population = sorted(population, key=lambda i: i['_fitness'], reverse=True)


    ################################################################################
    # Evolution Operators
    ################################################################################

    def crossover_individuals(self, individual1, individual2):
        """Return a new individual created by randomly taking attributes from two existing individuals."""
        new_individual = self.clone_individual(individual1)

        for field in new_individual.keys():
            if random.random() > 0.5:
                new_individual[field] = individual2[field]

        return new_individual


    def mutate_individual(self, individual):
        """Return a new individual created by randomly mutating an attribute in an existing individual."""
        new_individual = self.clone_individual(individual)

        parameter_keys = [field for field in list(new_individual.keys()) if not field.startswith('_')]
        new_individual[parameter_keys[math.floor(random.random() * len(parameter_keys))]] = random.random()

        return new_individual


    def create_random_population(self):
        """Create a new random population."""
        population = []

        for i in range(0, self.population_size):
            population.append(self.get_new_individual())

        return population
