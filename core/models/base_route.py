import math
import random
from typing import List
from copy import deepcopy
from core.models.city import City

class BaseRoute:
    """Base class for Route implementation"""
    
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
            total_distance += current_city.distance(next_city)
        self.distance = total_distance
        return total_distance

    def copy(self):
        new_cities = deepcopy(self.cities)
        return self.__class__(new_cities)

    def shuffle(self):
        random.shuffle(self.cities)
        self.distance = self.calculate_distance()
