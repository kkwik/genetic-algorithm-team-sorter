from player import Player
import random

from typing import List
from typing import Any

# Represents a team
class Chromosome:
    genes: List[Player] = []

    def __init__(self, players: List[Player]) -> None:
        if len(players) != 9:
            raise ValueError('ERROR: Chromosome does not have 9 values')
        
        self.genes = players
    
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, self.__class__):
            return self.toString() == other.toString()
        else:
            return False

    def __hash__(self) -> int:
        return hash(self.toString())

    # Will take a list of players and generate a random chromosome from them
    @staticmethod
    def createRandom(players: List[Player]) -> Chromosome:
        if len(players) < 9:
            raise ValueError('ERROR: Not enough players provided')
        return Chromosome(random.sample(players, 9))

    def calculateFitness(self) -> int:
        sum = 0
        for i, player in enumerate(self.genes):
            sum += player.scores[i]

        # sum /= 9
        return sum

    def toString(self) -> str:
        return f'{[player.name for player in self.genes]}'
