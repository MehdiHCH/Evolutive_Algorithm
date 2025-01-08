import math
import random
from typing import List
from copy import deepcopy
from pyproj import Proj
from core.models.city import City

class BaseRoute:
    """Base class for Route implementation"""
    
    def __init__(self, cities: List[City] = None, randomize=False, utm_zone=30, ellps="WGS84"):
        """
        Initialize a BaseRoute object.

        Parameters:
        - cities: List of City objects with longitude and latitude attributes.
        - randomize: Whether to shuffle the cities randomly.
        - utm_zone: UTM zone for projection (default: 30).
        - ellps: Reference ellipsoid for projection (default: "WGS84").
        """
        self.cities = cities if cities else []
        self.proj = Proj(proj="utm", zone=utm_zone, ellps=ellps)

        # Convert geographic coordinates to UTM
        for city in self.cities:
            city.x, city.y = self.proj(city.longitude, city.latitude)

        if randomize:
            random.shuffle(self.cities)
        self.distance = self.calculate_distance()

    def calculate_distance(self):
        """Calculate the total distance of the route."""
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

    def copy(self):
        """Create a deep copy of the route."""
        new_cities = deepcopy(self.cities)
        return self.__class__(new_cities)

    def shuffle(self):
        """Shuffle the order of cities in the route."""
        random.shuffle(self.cities)
        self.distance = self.calculate_distance()
