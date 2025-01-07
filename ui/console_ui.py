def visualize_console_ui(route):
    print("\n=== Visualisation Console ===")
    print("Itinéraire optimal :", " -> ".join(str(city.ID) for city in route.cities))
    print(f"Distance optimale : {route.distance:.2f}")