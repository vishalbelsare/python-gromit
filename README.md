# Gromit

Gromit is a pure-Python module that provides a very simple evolutionary algorithm.  The module was originally going to be named Wallace (after [Alfred Russel Wallace](https://en.wikipedia.org/wiki/Alfred_Russel_Wallace),) but that name was already taken.

When should you use Gromit?  There are a lot of options in Python with evolutionary programming.  Gromit was written to provide a very simple evolutionary algorithm for optimizing parameters.  It aims to be easy to use for a certain class of problems.   It does not have many advanced features, optimizations, or even parallelization.  If you have a simple task of optimizing parameters that could fit this simple model and perform well enough without parallelization, then Gromit may be a good fit.  Otherwise, it is better to look elsewhere.

# Usage

## Concepts

Gromit creates a `population` of `individuals`.  Each individual is composed of a number of fields, which are each a float with a value from `0` to `1`.

In order to use Gromit you need to provide a `schema` and a `fitness_handler`.

The `schema` is simply a list of fields.  For example:

```python
schema = ['age', 'color', 'shape']
```

The `fitness_handler` is a function that takes an `individual` as a parameter.  The `individual` is actually a `dict` with each of the fields in the `schema` in it along with its value from 0 to 1.  The fitness handler normally returns a number (though any value that can be sorted would work.)  The range of the values has no meaning to the algorithm.  An `individual` with a higher fitness than another is considered to be more fit.


## Example


### General usage

```python
from gromit import Gromit


# Create a gromit object by providing a schema (list of attributes) and a
# callback function.  Our attributes will be for an optimal pet.
gromit = Gromit(
    ['size', 'number_of_heads', 'is_domesticated', 'is_fluffy'],
    fitness_handler)


# Lets check the fitness of a pet by giving points based on the attributes
def fitness_handler(individual):
    # First, convert the attributes which are all floats from 0 to 1
    # to their real values
    size = individual['size'] * 10 + 0.01 # Number of feet tall
    number_of_heads = int(individual['number_of_heads'] * 3)
    is_domesticated = individual['is_domesticated'] <= 0.3 # 30% are domesticated
    is_fluffy = individual['is_fluffy'] <= 0.5 # 50% are fluffy

    points = 0
    # The further it is from our ideal size of 2 feet, take points away
    points -= abs(size - 2) / 4

    if number_of_heads == 0: # Headless pets are freaky!  Penalize them.
        points -= 50
    else: # One or more heads.  Bonus!
        points += 10

    points += 10 if is_fluffy else -10
    points += 30 if is_domesticated else -30

    return points


# Walk through 100 generations of evolution
for generation in range(0, 100):
   max_fitness = gromit.evolve()
   print("Generation %d: max fitness is %f" % (generation, max_fitness))


most_fit_individual = gromit.get_most_fit_individual()
print(("Most fit individual's attributes:\n" + \
       "   %(size).2f feet, %(number_of_heads)d heads\n" + \
       "   %(is_domesticated)s domesticated, %(is_fluffy)s fluffy") % {
           'size': individual['size'] * 10 + 0.01,
           'number_of_heads': int(individual['number_of_heads'] * 3),
           'is_domesticated': 'not' if individual['is_domesticated'] > 0.3 else '',
           'is_fluffy': 'not' if individual['is_fluffy'] > 0.5 else '',
       })
```


### Initialization

```python
# Create a gromit object by providing a schema and callback function
gromit = Gromit(['x', 'y'],
                fitness_handler)
```


The `Gromit()` function can also supports the following optional parameters:
* `population_size` - The number of individuals to maintain for each generation. (default 30)
* `copy_weight`, `mutate_weight`, `crossover_weight` - Relative weighting to determine the percentage of the new population is created from each operator. (default is 1 for each, so each get 33.33%)
* `kill_percent` - Percent of the weakest individuals to kill off each generation and replace with new randomized individuals.  The individuals purged are not candidates for the operators to use. (default is .1, meaning 10%)
* `new_individual_handler` - A callback for every time a new individual is created.  This function should take an individual as an argument and may modify it.


### Fitness Handler

A fitness handler is a function that takes an individual and returns a fitness value, where greater values imply higher fitness.


```python
def fitness_handler(individual):
    # Each parameter is a float from 0 to 1
    # To make the parameters usable for our purpose, we convert them to numbers from 0 to 32.
    x = individual['x'] * 32
    y = individual['y'] * 32

    # A number from 0 to 1 can be made into anything in the fitness operator
    # For example, if we need a number from 1000 to 2000
    x = individual['x'] * 1000 + 1000

    # Or if we need a boolean
    x = individual['x'] > 0.5

    # Return some evaluation of the parameters so that the higher the result
    # implies higher fitness
    return x / y
```
