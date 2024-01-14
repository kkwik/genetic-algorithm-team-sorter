from player import Player
import random

class Chromosome:
    genes = []

    def __init__(self, players):
        if len(players) != 9:
            raise ValueError('ERROR: Chromosome does not have 9 values')
        
        self.genes = players
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.toString() == other.toString()
        else:
            return False

    def __hash__(self):
        return hash(self.toString())

    # Will take a list of players and generate a random chromosome from them
    @staticmethod
    def createRandom(players):
        if len(players) < 9:
            raise ValueError('ERROR: Not enough players provided')
        return Chromosome(random.sample(players, 9))

    def calculateFitness(self):
        sum = 0
        for i, player in enumerate(self.genes):
            sum += player.scores[i]

        # sum /= 9
        return sum

    def toString(self):
        return f'{[player.name for player in self.genes]}'
