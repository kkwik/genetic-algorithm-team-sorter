from chromosome import Chromosome
from player import Player
import random

from typing import List

# Class representing the population of the GA
class Population:
    population_size: int = 100
    selected_amount: int = 50
    tournament_size: int = 10
    replaced_each_generation: int = 70
    mutation_chance: float = 0.5

    population: List[Chromosome] = []
    alleles: List[Player] = []
    parents: List[Chromosome] = []
    children: List[Chromosome] = []

    def __init__(self, population_size: int, selected_amount: int, tournament_size: int, replaced_each_generation: int, mutation_chance: float, alleles: List[Player]) -> None:
        self.population_size = population_size
        self.selected_amount = selected_amount
        self.tournament_size = tournament_size
        self.replaced_each_generation = replaced_each_generation
        self.mutation_chance = mutation_chance
        self.alleles = alleles

    # Create a random population of Chromosomes from the Players passed into the Population at construction
    # Duplicate Chromosomes are not allowed
    def initializeRandom(self) -> None:
        self.population = []
        self.parents = []
        self.children = []
        while len(self.population) < self.population_size:
            individual = Chromosome.createRandom(self.alleles)
            if individual not in self.population:
                self.population.append(individual)

    # Returns the highest fitness within the population
    def maxFitness(self) -> int:
        return max([chromosome.calculateFitness() for chromosome in self.population])

    # Run tournament selection to identify parents
    def tournamentSelection(self) -> None:
        parents: List[Chromosome] = []

        while len(parents) < self.selected_amount:
            tournament_participants = random.sample(self.population, self.tournament_size)
            winner = sorted(tournament_participants, key=lambda x: x.calculateFitness(), reverse=True)[0]
            parents.append(winner)
        
        self.parents = parents

    # Perform single point crossover
    def performCrossover(self, parents: List[Chromosome]) -> List[Chromosome]:
        crossover_point = random.randint(1, 8)
        parent0_l = parents[0].genes[:crossover_point]
        parent1_r = parents[1].genes[crossover_point:]

        child0 = Chromosome(parent0_l + parent1_r)

        parent0_r = parents[0].genes[crossover_point:]
        parent1_l = parents[1].genes[:crossover_point]

        child1 = Chromosome(parent1_l + parent0_r)

        # If the crossover would create an invalid child, return nothing
        if len(set(child0.genes)) != 9 or len(set(child1.genes)) != 9:
            return []

        return [child0, child1]

    # Run crossover on parents
    def crossover(self) -> None:
        children: List[Chromosome] = []

        while len(children) < self.replaced_each_generation:
            parents = random.sample(self.parents, 2)
            children.extend(self.performCrossover(parents))
        self.children = children

    # Do a reversal of two alleles
    def doMutate(self, individual: Chromosome) -> Chromosome:
        # Choose gene to start at and swap it and the next gene
        start = random.randint(0, 7)
        tmp = individual.genes[start]
        individual.genes[start] = individual.genes[start+1]
        individual.genes[start+1] = tmp
        return individual

    # Go through the new children and perform mutation based on chance
    def mutate(self) -> List[Chromosome]:
        result = []
        for individual in self.children:
            if random.random() < self.mutation_chance:
                individual = self.doMutate(individual)
                result.append(individual)
        return result

    # Remove underperforming individuals from the population
    def cull(self) -> None:
        self.population = sorted(self.population, key=lambda x: x.calculateFitness())[self.replaced_each_generation:]
    
    # Fill the population after culling with the generated children
    def replace(self) -> None:
        self.population += self.children

    # Sort the population based on fitness
    def sort(self) -> None:
        self.population = sorted(self.population, key=lambda x: x.calculateFitness(), reverse=True)

    # Function to run through all the steps of a generation for the population
    def runGeneration(self) -> None:
        self.tournamentSelection()  # Select parents for crossover
        self.crossover()            # Crossover
        self.mutate()               # Mutate
        self.cull()                 # Keep only the best from the current generation
        self.replace()              # Replace lost individuals with new generation
        self.sort()


