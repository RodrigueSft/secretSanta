import unittest

from SecretSantaGenerator import SecretSantaGenerator


class Test(unittest.TestCase):

    def test_init_secret_santa(self):
        print("Start init_secret_santa test\n")
        people = ["Florent", "Jessica", "Coline", "Emilien", "Ambroise", "Bastien"]
        couples = [("Florent", "Jessica"), ("Coline", "Emilien")]
        santa_generator = SecretSantaGenerator(people, couples)

        self.assertEqual(santa_generator.people, people)
        self.assertEqual(santa_generator.couples, couples)
        self.assertEqual(santa_generator.pairs, [])

    @staticmethod
    def secret_santa_validator(people, couples, pairs):
        l1, l2 = list(map(list, zip(*pairs)))
        if len(people) != len(set(l1)):
            print(f"Someone gave 2 gifts: {l1}")
            return False
        if len(people) != len(set(l2)):
            print(f"Someone received 2 gifts: {l2}")
            return False
        for g, r in pairs:
            if (g, r) in couples or (r, g) in couples:
                print(f"A couple has been matched together: {g, r}")
                return False
        return True

    def test_secret_santa_validator_good_0(self):
        people = ["Florent", "Jessica", "Coline"]
        couples = []

        pairs = [("Florent", "Jessica"), ("Jessica", "Coline"), ("Coline", "Florent")]
        self.assertEqual(self.secret_santa_validator(people, couples, pairs), True)

    def test_secret_santa_validator_good_1(self):
        people = ["Florent", "Jessica", "Coline", "Emilien", "Ambroise", "Bastien"]
        couples = [("Florent", "Jessica"), ("Coline", "Emilien")]

        pairs = [('Florent', 'Emilien'), ('Jessica', 'Bastien'), ('Coline', 'Jessica'), ('Emilien', 'Ambroise'), ('Ambroise', 'Florent'), ('Bastien', 'Coline')]
        self.assertEqual(self.secret_santa_validator(people, couples, pairs), True)

    def test_secret_santa_validator_bad_2_gifter(self):
        people = ["Florent", "Jessica", "Coline"]
        couples = []

        pairs = [("Florent", "Jessica"), ("Florent", "Coline"), ("Coline", "Florent")]
        self.assertEqual(self.secret_santa_validator(people, couples, pairs), False)

    def test_secret_santa_validator_bad_2_receiver(self):
        people = ["Florent", "Jessica", "Coline"]
        couples = []

        pairs = [("Florent", "Jessica"), ("Jessica", "Florent"), ("Coline", "Florent")]
        self.assertEqual(self.secret_santa_validator(people, couples, pairs), False)

    def test_secret_santa_validator_bad_couple_0(self):
        people = ["Florent", "Jessica", "Coline", "Emilien"]
        couples = [("Florent", "Jessica")]

        pairs = [("Florent", "Jessica"), ("Jessica", "Coline"), ("Coline", "Emilien"), ("Emilien", "Florent")]
        self.assertEqual(self.secret_santa_validator(people, couples, pairs), False)

    def test_secret_santa_validator_bad_couple_1(self):
        people = ["Florent", "Jessica", "Coline", "Emilien"]
        couples = [("Florent", "Jessica")]

        pairs = [("Jessica", "Florent"), ("Coline", "Jessica"), ("Emilien", "Coline"), ("Florent", "Emilien")]
        self.assertEqual(self.secret_santa_validator(people, couples, pairs), False)


unittest.main()
