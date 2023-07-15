import random


class SecretSantaGenerator:
    people = []
    couples = []
    pairs = []

    def __init__(self, people, couples):
        self.people = people
        self.couples = couples

    def __repr__(self) -> str:
        return f"{type(self).__name__}:\n people={self.people},\n couple={self.couples},\n pairs={self.pairs}\n"

    def generate(self):
        # prep work
        people_set = set(self.people)
        s = dict()
        gifted = set()
        for person in self.people:
            s[person] = {person}
        for a, b in self.couples:
            s[a].add(b)
            s[b].add(a)

        for p in self.people:
            available = people_set ^ (s[p] | gifted)
            # reset if receivers is empty because dead end
            receivers = random.sample(available, 1)

            self.pairs.append((p, receivers[0]))
            gifted.add(receivers[0])
            s[receivers[0]].add(p)

