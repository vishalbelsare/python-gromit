#!/usr/bin/env python3

from gromit import Gromit

# This is a simple example of usage of the Gromit module.  It attempts
# to find optimal parameters of 'x' and 'y', so that 'x' to power of
# 'y' equals 12345.  The problem has no significance and was only
# chosen to provide a simple demonstration of the usage of Gromit.


def fitness_handler(individual):
    # Each parameter is a float from 0 to 1
    # To make the parameters usable for our purpose, we convert them to numbers from 0 to 32.
    x = individual['x'] * 32
    y = individual['y'] * 32

    # Return the absolute value of the distance from the goal of x**y
    # == 12345 multiplied by -1.  We multiply by -1 since with the result, lower
    # numbers imply higher fitness.
    return abs(12345 - x ** y) * -1


def main():
    # Create a new Gromit object with 'x' and 'y' parameters
    gromit = Gromit(['x', 'y'], fitness_handler)

    # Evolve until the end result is within 0.25 of the target. (The
    # number is negative because we multiplied by -1 in the fitness
    # handler.)
    generation = 1
    while True:
        max_fitness = gromit.evolve()
        most_fit = gromit.get_most_fit_individual()

        # Log our current status along with the 'x' & 'y' of the most fit individual
        print("%(generation)4d: max fitness=%(max_fitness)f  (x=%(x)f, y=%(y)f)" % {
            'generation': generation,
            'max_fitness': max_fitness,
            'x': most_fit['x'] * 32, # 'x' & 'y' are displayed in their full 0 to 32 range
            'y': most_fit['y'] * 32
        })

        if max_fitness >= -0.25:
            break

        generation += 1


main()
