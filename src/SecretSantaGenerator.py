class SecretSantaGenerator:
    people = []
    couples = []
    pairs = []

    def __init__(self, people, couples):
        self.people = people
        self.couples = couples

    def __repr__(self) -> str:
        return f"{type(self).__name__}:\n people={self.people},\n couple={self.couples},\n pairs={self.pairs}\n"
