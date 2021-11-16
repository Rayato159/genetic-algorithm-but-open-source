# Created by HashTable159

# This file is the main file
# Use for run GA

from genetic_algorithm import GA

# Define lower bounds here
lower_bounds = [
    -5,
    -5
]

# Define upper bounds here
upper_bounds = [
    5,
    5
]

genetic = GA(
    parameters_num=len(lower_bounds),
    bits=16,
    population_num=100, 
    generation=100, 
    crossover_prob=0.95, 
    mutation_prob=0.03, 
    k=3,
    lower_bounds=lower_bounds,
    upper_bounds=upper_bounds
)

solution = genetic.run()