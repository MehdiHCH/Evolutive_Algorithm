from .models.city import City

def read_cities(filename):
    cities = []
    with open(filename, "r") as file:
        num_cities = int(file.readline().strip())
        for _ in range(num_cities):
            line = file.readline().strip().split()
            ID = int(line[0])
            x, y = map(float, line[1:])
            cities.append(City(ID, x, y))
    return cities


def save_cities(filename, coords):
    with open(filename, "w+") as file:
        num_cities = len(coords)
        file.write(f"{num_cities}\n")
        for idx, x, y in coords:
            line = f"{idx} {x} {y}"
            file.write(f"{line}\n")

