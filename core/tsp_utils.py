from .models.route import Route

def two_opt(route, i, k):
    if k <= i:
        return None
    new_cities = route.cities[:i] + route.cities[i:k+1][::-1] + route.cities[k+1:]
    new_route = Route(new_cities)
    new_route.calculate_distance()
    return new_route

def SuccesseurtwoOpt(route):
    max_value = float('-inf')
    best_successor = None

    for i in range(1, len(route.cities) - 1):
        for k in range(i + 1, len(route.cities)):
            new_route = two_opt(route, i, k)
            if new_route and (1 / new_route.distance) > max_value:
                max_value = 1 / new_route.distance
                best_successor = new_route

    return best_successor