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
