machines = [
    "http://52.47.166.137",
    "http://13.39.86.111",
    "http://51.44.22.52",
    "http://35.180.119.79",
]


def choisir(nom):
    x = sum(ord(a) for a in nom)
    return machines[x % len(machines)]


if __name__ == "__main__":
    m = choisir(input("quel est votre nom:"))
    print(f"connectez vous à {m}")
