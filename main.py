from core.models import Route
from core.io_utils import read_cities
from algorithms.sa import simulated_annealing
from ui.visualizer import plot_progress
import tkinter as tk

def main():
    cities = read_cities("berlin52.txt")
    initial_route = Route(cities)
    initial_route.calculate_distance()

    root = tk.Tk()
    canvas = tk.Canvas(root, width=750, height=500)
    canvas.pack()
    
    best_route = simulated_annealing(initial_route)
    print(f"Best distance: {best_route.distance}")
    root.mainloop()

if __name__ == "__main__":
    main()
