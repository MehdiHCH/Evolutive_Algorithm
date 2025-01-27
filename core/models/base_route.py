import math
import random
from typing import List
from copy import deepcopy
from core.models.city import City

class BaseRoute:
    """Base class for Route implementation"""

    def __len__(self):
        """Return the number of cities in the route."""
        return len(self.cities)  # Assuming `self.cities` is a list of cities

    
    def __init__(self, cities: List[City]=None, randomize=False):
        self.cities = cities if cities else []
        if randomize:
            random.shuffle(self.cities)
        self.distance = self.calculate_distance()

    def calculate_distance(self):
        total_distance = 0.0
        num_cities = len(self.cities)

        if num_cities == 0:
            return total_distance
        
        for i in range(num_cities):
            current_city = self.cities[i]
            next_city = self.cities[(i + 1) % num_cities]
            dx = current_city.x - next_city.x
            dy = current_city.y - next_city.y
            total_distance += math.sqrt(dx**2 + dy**2)
        self.distance = total_distance
        return total_distance

    def append(self, city_locations):
      self.cities.append(city_locations)  

    def remove(self, city_locations):
      self.cities.remove(city_locations) 

    def difference(self, cities):
      cities_to_remove = set(cities)
      self.cities = [city for city in self.cities if city not in cities_to_remove]
      return self.copy()

    def insert(self, index, city_locations):
      self.cities.insert(index, city_locations)

    def copy(self):
        new_cities = deepcopy(self.cities)
        return self.__class__(new_cities)
    
    def cities_list(self):
        """Access the cities as a list."""
        return self.cities
    
    def cities_to_list(self):
        """
        Converts the cities to a list of [id, x, y] format.

        Returns:
            A list of lists, where each inner list contains [id, x, y] of a city.
        """
        return [[city.ID, city.x, city.y] for city in self.cities]
