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
        try:
            population = self._initialize_population(initial_route)
            best_route = min(population, key=lambda x: x.distance)

            for generation in range(self.generations):
                try:
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
                except Exception as e:
                    print(f"Error during generation {generation}: {str(e)}")

            return best_route

        except Exception as e:
            print(f"Error during optimization: {str(e)}")
            raise

    def _initialize_population(self, initial_route: Route) -> List[Route]:
        try:
            population = [initial_route.copy()]
            for _ in range(self.population_size - 1):
                new_route = initial_route.copy()
                new_route.shuffle()
                population.append(new_route)
            return population
        except Exception as e:
            print(f"Error initializing population: {str(e)}")
            raise

    def _evolve_population(self, population: List[Route]) -> List[Route]:
        try:
            # Trier la population par distance (meilleur en premier)
            population.sort(key=lambda x: x.distance)
            elite = population[:self.elite_size]

            # Créer une nouvelle population via croisement et mutation
            new_population = elite.copy()
            while len(new_population) < self.population_size:
                try:
                    parent1 = random.choice(elite)
                    parent2 = random.choice(population)
                    child = self._crossover(parent1, parent2)
                    if random.random() < self.mutation_rate:
                        child.mutate()
                    new_population.append(child)
                except Exception as e:
                    print(f"Error during crossover or mutation: {str(e)}")

            return new_population
        except Exception as e:
            print(f"Error evolving population: {str(e)}")
            raise

    def _crossover(self, route1: Route, route2: Route) -> Route:
        try:
            # Implémentation du croisement ordonné (Ordered Crossover - OX)
            size = len(route1.cities)
            start, end = sorted(random.sample(range(size), 2))

            child_cities = [None] * size
            child_cities[start:end + 1] = route1.cities[start:end + 1]

            current_index = (end + 1) % size
            for city in route2.cities:
                if city not in child_cities:
                    while child_cities[current_index] is not None:
                        current_index = (current_index + 1) % size
                    child_cities[current_index] = city

            child = route1.copy()
            child.cities = child_cities
            child.calculate_distance()
            return child

        except Exception as e:
            print(f"Error during crossover: {str(e)}")
            raise

    def mutate(self, route: Route):
        """
        Implémentation avancée de la mutation par échange de deux villes (Swap Mutation).
        """
        try:
            size = len(route.cities)
            if size < 2:
                return  # Rien à faire si le nombre de villes est inférieur à 2

            i, j = random.sample(range(size), 2)
            route.cities[i], route.cities[j] = route.cities[j], route.cities[i]
            route.calculate_distance()

        except Exception as e:
            print(f"Error during mutation: {str(e)}")
            raise