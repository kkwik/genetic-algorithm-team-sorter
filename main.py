from player import Player
from chromosome import Chromosome
from population import Population
from data import players

from typing import Set
from typing import List

population = Population(population_size=1000, selected_amount=400, tournament_size=20, replaced_each_generation=500, mutation_chance=0.75, alleles=players)

max_fitness = 4*9   # Set a maximum fitness value, if this fitness value is exceeded the GA will stop
fitness = 0

max_iterations = 1000   # Set maximum generations of population
iteration = 0

max_stagnation = 30     # Set a limit to detect if the population's performance improvement plateaus 
stagnation = 0
old_fitness = 0

meta_runs = 20          # Amount of populations to generate and run
meta_results: Set[Chromosome] = set()


while len(meta_results) < meta_runs:

    population.initializeRandom()

    while iteration < max_iterations and fitness < max_fitness and stagnation < max_stagnation:
        old_fitness = fitness       # Track stagnation
        fitness = population.maxFitness()

        if fitness == old_fitness:
            stagnation += 1
        else:
            stagnation = 0

        population.runGeneration()

        iteration += 1
    winner = population.population[0]
    print(f'{winner.toString()} -> {winner.calculateFitness()}')
    iteration = 0
    stagnation = 0
    fitness = 0

   
    meta_results.add(winner)

print()
print(f'Meta Results')
meta_results_list: List[Chromosome] = list(meta_results)
meta_results_list = sorted(meta_results_list, key=lambda x: x.calculateFitness(), reverse=True)
for i, result in enumerate(meta_results):
    print(f'{i}. {result.toString()} -> {result.calculateFitness()}')

