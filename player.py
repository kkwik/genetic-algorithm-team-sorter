
class Player:
    name = ''
    scores = []

    def __init__(self, name: str, scores):
        self.name = name

        if len(scores) != 9:
            raise ValueError('ERROR: Player {name} does not have 9 values')
        self.scores = scores

