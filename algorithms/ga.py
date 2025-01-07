import random
from typing import List
from core.models.route import Route
from algorithms.base import TSPAlgorithm

class GeneticAlgorithm(TSPAlgorithm):
    def __init__(self, population_size=100, generations=1000, elite_size=20,
                 mutation_rate=0.01, progress_callback=None):
        super().__init__(progress_callback)
        self.population_size = population_size
        self.generations = generations
        self.elite_size = elite_size
        self.mutation_rate = mutation_rate
    
    def optimize(self, initial_route: Route) -> Route:
        population = self._initialize_population(initial_route)
        best_route = min(population, key=lambda x: x.distance)
        
        for generation in range(self.generations):
            population = self._evolve_population(population)
            current_best = min(population, key=lambda x: x.distance)
            
            if current_best.distance < best_route.distance:
                best_route = current_best.copy()
            
            self.update_progress(
                current_route=current_best,
                generation=generation,
                population_size=len(population),
                mutation_rate=self.mutation_rate,
                best_distance=best_route.distance
            )
        
        return best_route
    
    def _initialize_population(self, initial_route: Route) -> List[Route]:
        population = [initial_route.copy()]
        for _ in range(self.population_size - 1):
            new_route = initial_route.copy()
            new_route.shuffle()
            population.append(new_route)
        return population
    
    def _evolve_population(self, population: List[Route]) -> List[Route]:
        # Implementation of selection, crossover, and mutation
        # This is a simplified version
        population.sort(key=lambda x: x.distance)
        elite = population[:self.elite_size]
        
        # Create new population through crossover and mutation
        new_population = elite.copy()
        while len(new_population) < self.population_size:
            parent1 = random.choice(elite)
            parent2 = random.choice(population)
            child = self._crossover(parent1, parent2)
            if random.random() < self.mutation_rate:
                child.mutate()
            new_population.append(child)
            
        return new_population
    
    def _crossover(self, route1: Route, route2: Route) -> Route:
        # Implement ordered crossover (OX)
        # This is a simplified version
        child = route1.copy()
        child.shuffle()