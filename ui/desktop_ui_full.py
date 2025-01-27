import tkinter as tk
from tkinter import ttk, PhotoImage
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from core.utils import get_scale, spherical_to_cartesian
from typing import Optional
from tqdm import tqdm
from itertools import cycle

colors = cycle(["blue", "red", "green", "purple", "orange", "brown"])
iterations_list = []
distances_list = []
best_distances_list = []
color_list = []
algorithm_list = []

class TSPVisualizerWindow:
    def __init__(self, route, algorithms, total_iterations):
        """
        Initialize the TSP Visualizer Window.

        Args:
            route (Route): Initial route to visualize.
            algorithms (dict): Dictionary of algorithms with their classes and default parameters.
            total_iterations (int): Total number of iterations for progress tracking.
        """
        # self.name_algorithm = name_algorithm
        self.route = route
        self.algorithms = algorithms
        self.canvas_size = (700, 750)
        self.padding = 5
        self.min_values = self.max_values = None
        self.scale = self._calculate_scale(route)
        self.original_scale = self.scale
        self.offset_x = self.canvas_size[0] * 0.20
        self.offset_y = self.canvas_size[1] * 0.05

        self.total_iterations = total_iterations
        
        # Initialize the window
        self.root = tk.Tk()
        self.root.title("TSP Optimization Visualization")
        self.root.geometry("1400x800")
        self.root.state("zoomed")  # Open in fullscreen

        # Initialize selected algorithm and parameters
        self.selected_algorithm = tk.StringVar(value=list(algorithms.keys())[0])
        self.parameters_vars = {}

        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left panel for visualization and controls
        self._create_left_panel(main_container)

        # Right panel for progress information
        self._create_right_panel(main_container)

        # Bind canvas resize
        self.canvas.bind("<Configure>", self.on_resize)

        # Draw initial route
        self.draw_route(route)

        # Populate parameters UI
        self.update_parameters_ui()

    def _create_left_panel(self, parent):
        """Create the left panel for visualization and controls."""
        left_panel = ttk.Frame(parent)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Control panel
        control_panel = ttk.Frame(left_panel)
        control_panel.pack(fill=tk.X, pady=10)

        # Algorithm dropdown
        ttk.Label(control_panel, text="Algorithm:").pack(side=tk.LEFT, padx=5)
        self.algorithm_dropdown = ttk.Combobox(
            control_panel,
            textvariable=self.selected_algorithm,
            values=list(self.algorithms.keys()),
            state="readonly",
            width=20,
        )
        self.algorithm_dropdown.pack(side=tk.LEFT, padx=5)
        self.algorithm_dropdown.bind("<<ComboboxSelected>>", self.update_parameters_ui)

        # Start button
        ttk.Button(control_panel, text="Start Optimization", command=self.start_optimization).pack(side=tk.LEFT, padx=5)

        # Parameters UI
        self.params_frame = ttk.LabelFrame(left_panel, text="Algorithm Parameters")
        self.params_frame.pack(fill=tk.X, pady=10, padx=10)

        # Canvas for route visualization
        self.canvas = tk.Canvas(left_panel, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def _create_right_panel(self, parent):
        """Create the right panel for progress information."""
        right_panel = ttk.Frame(parent)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Metrics
        self.metrics_frame = ttk.LabelFrame(right_panel, text="Progress Metrics")
        self.metrics_frame.pack(fill=tk.X, pady=10)

        # Current iteration
        self.iteration_var = tk.StringVar(value="Iteration: 0")
        ttk.Label(self.metrics_frame, textvariable=self.iteration_var).pack(pady=5)

        # Current distance
        self.distance_var = tk.StringVar(value="Current Distance: 0")
        ttk.Label(self.metrics_frame, textvariable=self.distance_var).pack(pady=5)

        # Best distance
        self.best_distance_var = tk.StringVar(value="Best Distance: 0")
        ttk.Label(self.metrics_frame, textvariable=self.best_distance_var).pack(pady=5)

        # Graph for progress
        self.fig = Figure(figsize=(6, 4))
        self.ax = self.fig.add_subplot(111)
        self.canvas_plot = FigureCanvasTkAgg(self.fig, right_panel)
        self.canvas_plot.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=10)

        # Initialize progress tracking
        self.iterations = []
        self.distances = []
        self.best_distances = []

    def update_parameters_ui(self, event=None):
        """Update the UI with parameters for the selected algorithm."""
        # Clear existing widgets
        for widget in self.params_frame.winfo_children():
            widget.destroy()

        # Get parameters of the selected algorithm
        algorithm_name = self.selected_algorithm.get()
        algorithm_params = self.algorithms[algorithm_name]["params"]

        # Create input fields for each parameter
        self.parameters_vars = {}
        for i, (param, value) in enumerate(algorithm_params.items()):
            ttk.Label(self.params_frame, text=f"{param}:").grid(row=i, column=0, padx=5, pady=2, sticky="e")
            param_var = tk.DoubleVar(value=value) if isinstance(value, (int, float)) else tk.StringVar(value=value)
            self.parameters_vars[param] = param_var
            ttk.Entry(self.params_frame, textvariable=param_var, width=10).grid(row=i, column=1, padx=5, pady=2, sticky="w")

    def start_optimization(self):
        """Start the optimization process."""
        algorithm_name = self.selected_algorithm.get()
        algorithm_class = self.algorithms[algorithm_name]["class"]
        algorithm_list.append(algorithm_name)
        # Parse parameters
        params = {}
        for param, var in self.parameters_vars.items():
            value = var.get()
            # Convert to int if it's a whole number, otherwise leave as float or string
            params[param] = int(value) if isinstance(value, float) and value.is_integer() else value

        # Initialize progress tracker
        progress_tracker = ProgressTracker(self, total_iterations=self.total_iterations)

        # Instantiate and run the algorithm
        optimizer = algorithm_class(**params, progress_callback=progress_tracker)
        best_route = optimizer.optimize(self.route)

        # Draw the final route
        self.draw_route(best_route)

    def _calculate_scale(self, route):
        """Calculate appropriate scale for the visualization."""
        if not route or not route.cities:
            return 0.4

        scale, self.min_values, self.max_values, self.padding = get_scale(
            spherical_coords=map(lambda city: (city.ID, city.x, city.y), route.cities),
            canvas_size=self.canvas_size,
            padding=self.padding,
        )

        return scale

    def draw_route(self, route):
        """Draw the current route on the canvas."""
        if not route:
            return
        self.canvas.delete("all")

        # Draw connections between cities
        for i in range(len(route.cities)):
            city_a = route.cities[i]
            city_b = route.cities[(i + 1) % len(route.cities)]

            x1, y1 = self._get_canvas_coords(city_a)
            x2, y2 = self._get_canvas_coords(city_b)

            self.canvas.create_line(x1, y1, x2, y2, fill="blue", arrow=tk.LAST)

        # Draw city points and labels
        for city in route.cities:
            x, y = self._get_canvas_coords(city)
            self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="red")
            self.canvas.create_text(x + 10, y + 6, text=str(city.ID), fill="black")

    def _get_canvas_coords(self, city):
        """Convert spherical coordinates to canvas coordinates."""
        idx, x, y = spherical_to_cartesian(
            spherical_coords=(city.ID, city.x, city.y),
            scale=self.scale,
            min_values=self.min_values,
            max_values=self.max_values,
            padding=self.padding,
        )
        return x + self.offset_x, y + self.offset_y

    def on_resize(self, event):
        """Handle canvas resizing."""
        self.canvas_size = (event.width, event.height)
        self.draw_route(self.route)

    def update_progress(self, progress_info, color):
        """Update progress information during optimization."""
        current_route = progress_info["current_route"]
        if current_route is None:
            return

        iteration = progress_info.get("iteration", 0)
        current_distance = current_route.distance
        best_distance = progress_info.get("best_distance", current_distance)

        if iteration == 1:
            # algorithm_list.append(self.name_algorithm)
            iterations_list.append(list(self.iterations))
            distances_list.append(list(self.distances))
            best_distances_list.append(list(self.best_distances))
            color_list.append(color)
            self.iterations.clear()
            self.distances.clear()
            self.best_distances.clear()

        # Update route visualization
        self.draw_route(current_route)

        # Update metrics
        self.iteration_var.set(f"Iteration: {iteration}")
        self.distance_var.set(f"Current Distance: {current_distance:.2f}")
        self.best_distance_var.set(f"Best Distance: {best_distance:.2f}")

        # Update graph
        self.iterations.append(iteration)
        self.distances.append(current_distance)
        self.best_distances.append(best_distance)

        self.ax.clear()
        
        if iteration == 1:
            self.ax.cla()
        for i in range(len(iterations_list)):
            if iterations_list[i]:
                self.ax.plot(iterations_list[i], distances_list[i], color=color_list[i], label=algorithm_list[i-1])

        self.ax.plot(self.iterations, self.distances, color=color, label=algorithm_list[-1])

        
        self.ax.set_xlabel("Iteration")
        self.ax.set_ylabel("Distance")
        self.ax.legend()
        self.ax.grid(True)
        self.canvas_plot.draw()

        self.route = current_route

        self.root.update()


class ProgressTracker:
    def __init__(self, desktop_window: TSPVisualizerWindow = None, total_iterations: Optional[int] = None):
        self.desktop_window = desktop_window
        self.total_iterations = total_iterations
        self.best_distance = float("inf")
        self.color = next(colors)
        # Initialize progress bar if total iterations is known
        if self.total_iterations:
            self.progress_bar = tqdm(
                total=total_iterations,
                desc="Optimizing route",
                unit="iterations",
                bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [elapsed: {elapsed}, remaining: {remaining}]",
            )

    def __call__(self, **progress_info):
        """
        Update progress information.
        """
        current_route = progress_info["current_route"]
        iteration = progress_info.get("iteration", 0)
        
        if self.progress_bar:
            self.progress_bar.n = iteration
            self.progress_bar.set_description(f"Current Distance: {current_route.distance:.2f}")
            self.progress_bar.refresh()

        if "best_distance" in progress_info:
            self.best_distance = min(self.best_distance, progress_info["best_distance"])

        self.desktop_window.update_progress(progress_info, self.color)
        if iteration == 1:
            self.color = next(colors)
            


    def close(self):
        """Clean up resources."""
        if self.progress_bar:
            self.progress_bar.close()


def visualize_desktop_ui(route, algorithms, total_iterations):
    """Launch the desktop UI for TSP visualization."""
    window = TSPVisualizerWindow(route, algorithms, total_iterations)
    window.root.mainloop()
