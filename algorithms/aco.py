import sys
import os
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_path)

import random
import math
from typing import List
from core.models.route import Route
from core.models.city import City
from algorithms.base import TSPAlgorithm
import numpy as np

class Colony(TSPAlgorithm):
    def __init__(self, num_ants=50, alpha=1.0, beta=5.0, evaporation_rate=0.5, pheromone_deposit=100.0,progress_callback=None):
        super().__init__(progress_callback)
        """
        Initialize the Ant Colony Optimization algorithm with given parameters.
        """
        self.num_ants = num_ants
        self.num_iterations = self.progress_callback.total_iterations
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.pheromone_deposit = pheromone_deposit


    @staticmethod
    def initialize_pheromone_matrix(route):
        """
        Initialize the pheromone matrix with default values.
        """
        return dict.fromkeys([(source_location,destination_location) for source_location in route.cities for destination_location in route.cities if source_location != destination_location], 1)

    def get_pheromones(self, source_location, destination_location):
        return self.pheromones[(source_location, destination_location)]

    def select_next_city(self, route, current_city, visited, pheromone_matrix):
        """
        Select the next city for an ant based on transition probabilities.
        """
        probabilities = []
        unvisited_cities = [city for city in route.cities if city not in visited]

        for city in unvisited_cities:
            pheromone = pheromone_matrix[(current_city, city)] ** self.alpha
            heuristic = (1.0 / current_city.distance(city)) ** self.beta
            probabilities.append(pheromone * heuristic)
        probabilities = np.array(probabilities)
        probabilities_sum = np.sum(probabilities)
        if probabilities_sum == 0:
            return random.choice(unvisited_cities)
        probabilities /= probabilities_sum

        # Select next city based on probabilities
        return np.random.choice(unvisited_cities, p=probabilities)

    def update_pheromone_matrix(self, pheromone_matrix, all_paths, all_distances):
        """
        Update the pheromone levels on the matrix based on the paths taken by ants.
        """
        for key in pheromone_matrix:
            pheromone_matrix[key] *= (1 - self.evaporation_rate)

        # Add pheromones based on ant paths
        for path, distance in zip(all_paths, all_distances):
            pheromone_contribution = self.pheromone_deposit / distance
            for i in range(len(path) - 1):
                source = path[i]
                destination = path[i + 1]
                pheromone_matrix[(source, destination)] += pheromone_contribution
            # Add pheromones for the return to the starting city
            pheromone_matrix[(path[-1], path[0])] += pheromone_contribution

    def optimize(self, routes: Route):
        print("Optimizing route using Ant Colony Optimization...")
        """
        Perform the Ant Colony Optimization algorithm on the given route.
        """
        num_cities = len(routes)
        pheromone_matrix = Colony.initialize_pheromone_matrix(routes)
        best_path = None
        best_distance = float('inf')

        for iteration in range(1000):
            all_paths = []
            all_distances = []

            for ant in range(self.num_ants):
                visited = set()
                # current_city = City(0,565.00,575.00)
                current_city = routes.cities[0]
                path = [current_city]
                visited.add(current_city)

                while len(visited) < num_cities:
                    next_city = self.select_next_city(routes, current_city, visited, pheromone_matrix)
                    path.append(next_city)
                    visited.add(next_city)
                    current_city = next_city

                path_distance = sum(path[i].distance(path[i + 1]) for i in range(num_cities - 1))
                path_distance += path[-1].distance(path[0])  # Return to start
                all_paths.append(path)
                all_distances.append(path_distance)

                if path_distance < best_distance:
                    best_distance = path_distance
                    best_path = path
            self.update_progress(
            current_route=Route(best_path),
            best_distance=best_distance
            )
            self.update_pheromone_matrix(pheromone_matrix, all_paths, all_distances)
        return Route(best_path), best_distance
    

