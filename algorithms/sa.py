import random
import math
from typing import List
from core.models.route import Route
from algorithms.base import TSPAlgorithm

class SimulatedAnnealing(TSPAlgorithm):
    def __init__(self, initial_temp=1000, cooling_rate=0.995, min_temp=1e-8, 
                 progress_callback=None):
        super().__init__(progress_callback)
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate
        self.min_temp = min_temp
    
    def optimize(self, initial_route: Route) -> Route:
        current_route = initial_route.copy()
        best_route = current_route.copy()
        temp = self.initial_temp
        
        while temp > self.min_temp and self.iteration <= self.progress_callback.total_iterations:
            new_route = current_route.get_neighbor()
            delta = new_route.distance - current_route.distance
            
            if delta < 0 or random.random() < math.exp(-delta / temp):
                current_route = new_route
                if current_route.distance < best_route.distance:
                    best_route = current_route.copy()
            
            desktop_window = self.update_progress(
                current_route=current_route,
                temperature=temp,
                best_distance=best_route.distance
            )
            
            temp *= self.cooling_rate

            self.iteration += 1
        
        return best_route, desktop_window
