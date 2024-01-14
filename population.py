from chromosome import Chromosome
import random

class Population:
    population_size = 100
    selected_amount = 50
    tournament_size = 10
    replaced_each_generation = 70
    mutation_chance = 0.5

    population = []
    alleles = []
    parents = []
    children = []

    def __init__(self, population_size, selected_amount, tournament_size, replaced_each_generation, mutation_chance, alleles):
        self.population_size = population_size
        self.selected_amount = selected_amount
        self.tournament_size = tournament_size
        self.replaced_each_generation = replaced_each_generation
        self.mutation_chance = mutation_chance
        self.alleles = alleles

    def initializeRandom(self):
        self.population = []
        self.parents = []
        self.children = []
        while len(self.population) < self.population_size:
            individual = Chromosome.createRandom(self.alleles)
            if individual not in self.population:
                self.population.append(individual)

    def maxFitness(self):
        return max([chromosome.calculateFitness() for chromosome in self.population])

    def tournamentSelection(self):
        parents = []

        while len(parents) < self.selected_amount:
            tournament_participants = random.sample(self.population, self.tournament_size)
            winner = sorted(tournament_participants, key=lambda x: x.calculateFitness(), reverse=True)[0]
            parents.append(winner)
        
        self.parents = parents


    def performCrossover(self, parents):
        crossover_point = random.randint(1, 8)
        parent0_l = parents[0].genes[:crossover_point]
        parent1_r = parents[1].genes[crossover_point:]

        child0 = Chromosome(parent0_l + parent1_r)

        parent0_r = parents[0].genes[crossover_point:]
        parent1_l = parents[1].genes[:crossover_point]

        child1 = Chromosome(parent1_l + parent0_r)

        if len(set(child0.genes)) != 9 or len(set(child1.genes)) != 9:
            return []

        return [child0, child1]

    def crossover(self):
        children = []

        while len(children) < self.replaced_each_generation:
            parents = random.sample(self.parents, 2)
            children.extend(self.performCrossover(parents))
        self.children = children

    def doMutate(self, individual):
        # Choose gene to start at and swap it and the next gene
        start = random.randint(0, 7)
        tmp = individual.genes[start]
        individual.genes[start] = individual.genes[start+1]
        individual.genes[start+1] = tmp
        return individual

    def mutate(self):
        result = []
        for individual in self.children:
            if random.random() < self.mutation_chance:
                individual = self.doMutate(individual)
                result.append(individual)
        return result

    def cull(self):
        self.population = sorted(self.population, key=lambda x: x.calculateFitness())[self.replaced_each_generation:]
    
    def replace(self):
        self.population += self.children

    def sort(self):
        self.population = sorted(self.population, key=lambda x: x.calculateFitness(), reverse=True)

    def runGeneration(self):
        self.tournamentSelection()  # Select parents for crossover
        self.crossover()            # Crossover
        self.mutate()               # Mutate
        self.cull()                 # Keep only the best from the current generation
        self.replace()              # Replace lost individuals with new generation
        self.sort()


