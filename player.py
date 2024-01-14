from typing import List

# An allele in the Chromosome
class Player:
    name: str = ''
    scores: List[int] = []

    def __init__(self, name: str, scores: List[int]) -> None:
        self.name = name

        if len(scores) != 9:
            raise ValueError('ERROR: Player {name} does not have 9 values')
        self.scores = scores