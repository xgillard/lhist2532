machines = [
    "http://13.39.87.228",
    "http://13.39.105.229",
    "http://35.180.192.243",
    "http://35.180.131.5",
]


def choisir(nom):
    x = sum(ord(a) for a in nom)
    return machines[x % len(machines)]


if __name__ == "__main__":
    m = choisir(input("quel est votre nom:"))
    print(f"connectez vous à {m}")
