from SecretSantaGenerator import SecretSantaGenerator


def main():
    people = ["Florent", "Jessica", "Coline", "Emilien", "Ambroise", "Bastien"]
    couples = [("Florent", "Jessica"), ("Coline", "Emilien")]
    secret_santa = SecretSantaGenerator(people, couples)
    print(secret_santa)


if __name__ == "__main__":
    main()
