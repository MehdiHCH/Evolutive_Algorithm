import random
from typing import List
from core.models.route import Route
from algorithms.base import TSPAlgorithm

class EvolutionStrategy(TSPAlgorithm):
    def __init__(self, population_size=50, offspring_size=100, mutation_rate=0.2, 
                 max_generations=1000, progress_callback=None):
        super().__init__(progress_callback)
        self.population_size = population_size
        self.offspring_size = offspring_size
        self.mutation_rate = mutation_rate
        self.max_generations = max_generations

    def initialize_population(self, initial_route: Route) -> List[Route]:
        return [initial_route.random_permutation() for _ in range(self.population_size)]

    def mutate(self, route: Route) -> Route:
        if random.random() < self.mutation_rate:
            return route.random_swap()
        return route

    def recombine(self, parent1: Route, parent2: Route) -> Route:
        return parent1.crossover(parent2)

    def select_parents(self, population: List[Route]) -> List[Route]:
        return random.choices(population, weights=[1 / r.distance for r in population], k=2)

    def optimize(self, initial_route: Route) -> Route:
        population = self.initialize_population(initial_route)
        best_route = min(population, key=lambda r: r.distance)

        for generation in range(self.max_generations):
            offspring = []

            for _ in range(self.offspring_size):
                parent1, parent2 = self.select_parents(population)
                child = self.recombine(parent1, parent2)
                child = self.mutate(child)
                offspring.append(child)

            combined = population + offspring
            population = sorted(combined, key=lambda r: r.distance)[:self.population_size]

            current_best = min(population, key=lambda r: r.distance)
            if current_best.distance < best_route.distance:
                best_route = current_best

            self.update_progress(
                current_route=current_best,
                generation=generation,
                best_distance=best_route.distance
            )

        return best_route