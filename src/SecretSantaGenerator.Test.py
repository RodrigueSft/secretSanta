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


unittest.main()
