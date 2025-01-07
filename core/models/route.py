import math

class Route:
    def __init__(self, cities=None):
        self.cities = cities if cities else []
        self.distance = 0.0

    def calculate_distance(self):
        total_distance = 0.0
        num_cities = len(self.cities)
        for i in range(num_cities):
            current_city = self.cities[i]
            next_city = self.cities[(i + 1) % num_cities]
            dx = current_city.x - next_city.x
            dy = current_city.y - next_city.y
            total_distance += math.sqrt(dx**2 + dy**2)
        self.distance = total_distance