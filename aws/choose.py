machines = [
    "http://35.180.192.38",
    "http://13.37.215.229",
]


def choisir(nom):
    x = sum(ord(a) for a in nom)
    return machines[x % len(machines)]


if __name__ == "__main__":
    m = choisir(input("quel est votre nom:"))
    print(f"connectez vous à {m}")
