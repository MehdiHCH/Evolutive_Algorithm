from core.models.base_route import BaseRoute

class Route(BaseRoute):
    """Main Route class implementing the neighbor generation using 2-opt"""
    
    def get_neighbor(self):
        """
        Generate a neighbor using 2-opt swap.
        
        Returns:
            New Route object with the best 2-opt swap applied
        """
        from core.tsp_utils import SuccesseurtwoOpt
        
        best_cities = SuccesseurtwoOpt(self)
        if best_cities:
            return self.__class__(best_cities)
        return None
        """Return a string representation of the route."""
        return f"Route(cities={len(self.cities)}, distance={self.distance:.2f})"