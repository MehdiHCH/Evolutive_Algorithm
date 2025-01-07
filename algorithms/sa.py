import random
import math
from core.models.route import Route
from core.tsp_utils import SuccesseurtwoOpt

def simulated_annealing(initial_route, cooling_rate=0.93, Tstop=1e-8):
    current_route = initial_route
    best_route = Route(current_route.cities[:])
    best_route.calculate_distance()

    temperature = -initial_route.distance / math.log(0.5)
    while temperature > Tstop:
        neighbor_route = SuccesseurtwoOpt(current_route)
        if neighbor_route:
            delta = neighbor_route.distance - current_route.distance
            if delta < 0 or math.exp(-delta / temperature) > random.random():
                current_route = neighbor_route
                if neighbor_route.distance < best_route.distance:
                    best_route = Route(neighbor_route.cities[:])
                    best_route.calculate_distance()
        temperature *= cooling_rate

    return best_route
