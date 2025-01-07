from core.models.route import Route

def two_opt(cities, i, k):
    """
    Perform a 2-opt swap operation on a list of cities.
    
    Args:
        cities: List of cities
        i: First index
        k: Second index
    
    Returns:
        New list of cities with the segment reversed
    """
    if k <= i:
        return None
    return cities[:i] + cities[i:k+1][::-1] + cities[k+1:]

def SuccesseurtwoOpt(route_obj):
    """
    Find the best 2-opt swap for a given route.
    
    Args:
        route_obj: Route object containing cities and distance
    
    Returns:
        New list of cities with the best 2-opt swap applied
    """
    max_value = float('-inf')
    best_cities = None
    
    for i in range(1, len(route_obj.cities) - 1):
        for k in range(i + 1, len(route_obj.cities)):
            new_cities = two_opt(route_obj.cities, i, k)
            if new_cities:
                # Create a temporary route to calculate distance
                temp_route = route_obj.__class__(new_cities)
                temp_route.calculate_distance()
                if (1 / temp_route.distance) > max_value:
                    max_value = 1 / temp_route.distance
                    best_cities = new_cities
    
    return best_cities