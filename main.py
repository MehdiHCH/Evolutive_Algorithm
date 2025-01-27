import json
import os
import traceback
from core.models.route import Route
from core.io_utils import read_cities
from ui.desktop_ui_full import visualize_desktop_ui  # Import the new UI
from algorithms.sa import SimulatedAnnealing
from algorithms.ga import GeneticAlgorithm
from algorithms.es import EvolutionStrategy
from algorithms.aco import Colony


# Définitions des paramètres par défaut
DEFAULT_CONFIG = {
    "data_path": "data/maroc.txt",
    "random_init": True,
    "total_iterations": 1e3,
    "sa": {
        "initial_temp": 1000,
        "cooling_rate": 0.995,
        "min_temp": 1e-8
    },
    "ga": {
        "population_size": 1000,
        "generations": 1000,
        "elite_size": 10,
        "mutation_rate": 0.02
    },
    "es": {
        "population_size": 50,
        "offspring_size": 100,
        "mutation_rate": 0.2,
        "max_generations": 1000
    },
    "aco": {
        "num_ants": 50
    }

}


def load_config(config_file: str) -> dict:
    """
    Charger les configurations depuis un fichier JSON. Si le fichier est introuvable, utiliser les valeurs par défaut.

    Args:
        config_file: Chemin vers le fichier de configuration JSON.

    Returns:
        dict: Dictionnaire contenant les configurations des algorithmes.
    """
    if os.path.exists(config_file):
        try:
            with open(config_file, "r") as file:
                return json.load(file)
        except Exception as e:
            print(f"Erreur lors du chargement du fichier de configuration : {e}")
    print("Fichier de configuration introuvable ou invalide. Utilisation des valeurs par défaut.")
    return DEFAULT_CONFIG


def get_algorithm_classes(config: dict = None):
    """
    Return a dictionary of supported algorithms with their classes and default parameters.

    Returns:
        dict: Algorithm classes and their default parameters.
    """
    algorithms_config = config if bool(config) else DEFAULT_CONFIG

    return {
        "Simulated Annealing": {
            "class": SimulatedAnnealing,
            "params": algorithms_config["sa"]
        },
        "Genetic Algorithm": {
            "class": GeneticAlgorithm,
            "params": algorithms_config["ga"]
        },
        "Evolution Strategy": {
            "class": EvolutionStrategy,
            "params": algorithms_config["es"]
        },
        "Ant Colony": {
            "class": Colony,
            "params": algorithms_config["aco"]
        }
    }


def main():
    # Chemin par défaut du fichier de configuration
    CONFIG_FILE = "config/config.json"

    try:
        # Charger les configurations
        config = load_config(CONFIG_FILE)

        # Lire les villes depuis le fichier de données
        data_file = config["data_path"]
        cities = read_cities(data_file)
        if not cities:
            raise ValueError("Aucune ville chargée depuis le fichier de données.")

        # Créer l'itinéraire initial
        initial_route = Route(cities, randomize=config["random_init"])
        initial_route.calculate_distance()
        print(f"Distance initiale : {initial_route.distance:.2f}")

        # Charger les classes d'algorithmes et leurs paramètres
        algorithm_classes = get_algorithm_classes(config)

        # Passer les itinéraires et algorithmes à l'interface graphique
        visualize_desktop_ui(
            route=initial_route,
            algorithms=algorithm_classes,
            total_iterations = config["total_iterations"],
        )

    except Exception as e:
        print(f"Erreur : {str(e)}")
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
