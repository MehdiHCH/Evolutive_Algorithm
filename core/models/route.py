from core.models.base_route import BaseRoute
from copy import deepcopy
import random

class Route(BaseRoute):
    """Main Route class implementing the neighbor generation using 2-opt and crossover."""

    def get_neighbor(self):
        """
        Generate a neighbor using 2-opt swap.
        
        Returns:
            New Route object with the best 2-opt swap applied.
        """
        from core.tsp_utils import SuccesseurtwoOpt
        
        best_cities = SuccesseurtwoOpt(self)
        if best_cities:
            return self.__class__(best_cities)
        return None
    
    def random_permutation(self):
        """
        Generate a random permutation of the cities in the route.
        
        Returns:
            New Route object with cities shuffled randomly.
        """
        from copy import deepcopy
        import random

        new_route = deepcopy(self)  # Create a copy of the current route
        random.shuffle(new_route.cities)  # Shuffle the cities randomly
        new_route.calculate_distance()  # Recalculate the total distance
        return new_route

    def crossover(self, other: "Route") -> "Route":
        """
        Perform an Order Crossover (OX) between this route and another.
        
        Args:
            other: Another Route object to perform the crossover with.
        
        Returns:
            A new Route object representing the child of the crossover.
        """
        import random

        # Select two random crossover points
        start, end = sorted(random.sample(range(len(self.cities)), 2))

        # Take the segment from the first parent
        child_cities = [None] * len(self.cities)
        child_cities[start:end] = self.cities[start:end]

        # Fill in the rest from the second parent in order
        current_pos = end
        for city in other.cities:
            if city not in child_cities:
                if current_pos >= len(self.cities):
                    current_pos = 0
                child_cities[current_pos] = city
                current_pos += 1

        # Create a new Route with the child cities
        child_route = self.__class__(child_cities)
        child_route.calculate_distance()
        return child_route

    def random_swap(self):
        """
        Perform a mutation by swapping two random cities in the route.
        
        Returns:
            New Route object with two cities swapped.
        """
        from copy import deepcopy
        import random

        new_route = deepcopy(self)  # Create a copy of the current route
        idx1, idx2 = random.sample(range(len(self.cities)), 2)  # Select two random indices
        new_route.cities[idx1], new_route.cities[idx2] = new_route.cities[idx2], new_route.cities[idx1]  # Swap cities
        new_route.calculate_distance()  # Recalculate the distance
        return new_route

    def __str__(self):
        """Return a string representation of the route."""
        return f"Route(cities={len(self.cities)}, distance={self.distance:.2f})"