import random


class SecretSantaGenerator:
    people = []
    couples = []
    pairs = []

    TRY_ALLOWED = 5

    def __init__(self, people=None, couples=None):
        self.pairs = []
        if people is None:
            self.people = []
        else:
            self.people = people
        if couples is None:
            self.couples = []
        else:
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

        most_painfull_gifters = [x[0] for x in sorted(s.items(), key=lambda x: len(x[1]), reverse=True)]

        i = 0
        tmp = -1
        nb_try = 0

        def call_back_santa():
            nonlocal i
            i -= 1
            removed_pair = self.pairs.pop()
            print(f"removed_pair: {removed_pair}")
            gifted.remove(removed_pair[1])
            s[removed_pair[1]].remove(removed_pair[0])

        while i < len(most_painfull_gifters):
            p = most_painfull_gifters[i]
            available = people_set ^ (s[p] | gifted)

            if len(available) <= 0:
                if i <= 0:
                    print("Secret santa not possible")
                    return

                if tmp == i:
                    nb_try += 1
                else:
                    tmp = i

                if nb_try >= self.TRY_ALLOWED:
                    nb_try = 0
                    call_back_santa()

                call_back_santa()
                continue

            receivers = random.sample(available, 1)

            self.pairs.append((p, receivers[0]))
            gifted.add(receivers[0])
            s[receivers[0]].add(p)

            i += 1

