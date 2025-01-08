import argparse
from typing import Optional
from core.models.route import Route
from core.io_utils import read_cities
from algorithms.sa import SimulatedAnnealing
from algorithms.ga import GeneticAlgorithm
from algorithms.es import EvolutionStrategy
from ui.progress_tracker import ProgressTracker
from ui.desktop_ui import visualize_desktop_ui
from ui.web_ui import launch_web_ui
from ui.console_ui import visualize_console_ui
import traceback

def run_ui(ui_type: str, best_route: Optional[Route] = None) -> None:
    """
    Launch the specified user interface type.
    
    Args:
        ui_type: Type of UI to launch ('desktop', 'web', or 'console')
        best_route: The best route found by the algorithm
    """
    if ui_type == "desktop":
        visualize_desktop_ui(best_route)
    elif ui_type == "web":
        launch_web_ui(best_route)
    elif ui_type == "console":
        visualize_console_ui(best_route)
    else:
        print(f"UI Type '{ui_type}' not supported. Available options: desktop, web, console.")

def get_algorithm(algorithm_type: str, progress_tracker: ProgressTracker):
    """
    Factory function to create the appropriate algorithm instance.
    
    Args:
        algorithm_type: Type of algorithm to create ('sa', 'ga', or 'es')
        progress_tracker: Progress tracker instance for UI updates
        
    Returns:
        An instance of the specified algorithm
    """
    if algorithm_type == "sa":
        return SimulatedAnnealing(
            initial_temp=1000,
            cooling_rate=0.995,
            min_temp=1e-8,
            progress_callback=progress_tracker
        )
    elif algorithm_type == "ga":
        return GeneticAlgorithm(
            population_size=100,
            generations=1000,
            elite_size=20,
            mutation_rate=0.01,
            progress_callback=progress_tracker
        )
    elif algorithm_type == "es":
        return EvolutionStrategy(
            population_size=50,
            offspring_size=100,
            mutation_rate=0.2,
            max_generations=1000,
            progress_callback=progress_tracker
        )
    else:
        raise ValueError(f"Algorithm type '{algorithm_type}' not supported")

def main():
    # Configure command line arguments
    parser = argparse.ArgumentParser(description="Solve TSP using various algorithms")
    parser.add_argument(
        "--algorithm", type=str, default="sa",
        choices=["sa", "ga", "es"],
        help="Algorithm to use: 'sa' (Simulated Annealing), 'ga' (Genetic Algorithm), or 'es' (Evolution Strategy)"
    )
    parser.add_argument(
        "--ui", type=str, default="console",
        choices=["desktop", "web", "console"],
        help="User interface type"
    )
    parser.add_argument(
        "--data", type=str, default="data/berlin52.txt",
        help="Path to city data file"
    )
    parser.add_argument(
        "--random_init", type=bool, default=False,
        help="Initialize route randomly"
    )

    args = parser.parse_args()

    try:
        # Read cities from the specified file
        cities = read_cities(args.data)
        if not cities:
            raise ValueError("No cities loaded from the data file")

        # Create initial route
        initial_route = Route(cities, args.random_init)
        initial_route.calculate_distance()
        print(f"Initial distance: {initial_route.distance:.2f}")

        # Create progress tracker for UI updates
        progress_tracker = ProgressTracker(args.ui, total_iterations=1000)

        # Initialize and run selected algorithm
        algorithm = get_algorithm(args.algorithm, progress_tracker)
        best_route = algorithm.optimize(initial_route)

        # Print final results
        print(f"\nBest distance found: {best_route.distance:.2f}")
        print("Optimal route:", " -> ".join(str(city.ID) for city in best_route.cities))

        # Show final result in UI
        run_ui(args.ui, best_route)

    except Exception as e:
        print(f"Error: {str(e)}")
        traceback.print_exc()
        return 1

    return 0

if __name__ == "__main__":
    exit(main())