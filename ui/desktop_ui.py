import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class TSPVisualizerWindow:
    def __init__(self, route):
        self.root = tk.Tk()
        self.root.title("TSP Optimization Visualization")
        self.root.geometry("1200x800")
        
        # Create main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel for route visualization
        left_panel = ttk.Frame(main_container)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Route canvas
        self.canvas = tk.Canvas(left_panel, width=600, height=600, bg='white')
        self.canvas.pack(pady=10)
        
        # Right panel for progress information
        right_panel = ttk.Frame(main_container)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Progress metrics
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
        
        # Progress graph
        self.fig = Figure(figsize=(6, 4))
        self.ax = self.fig.add_subplot(111)
        self.canvas_plot = FigureCanvasTkAgg(self.fig, right_panel)
        self.canvas_plot.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Initialize progress tracking
        self.iterations = []
        self.distances = []
        self.best_distances = []
        
        # Initialize scale for route visualization
        self.scale = self._calculate_scale(route)
        
        # Draw initial route
        self.draw_route(route)
        
    def _calculate_scale(self, route):
        """Calculate appropriate scale based on city coordinates"""
        if not route.cities:
            return 0.4
            
        max_x = max(city.x for city in route.cities)
        max_y = max(city.y for city in route.cities)
        
        # Calculate scale to fit within 80% of canvas size
        scale_x = 480 / max_x if max_x > 0 else 1
        scale_y = 480 / max_y if max_y > 0 else 1
        
        return min(scale_x, scale_y)
        
    def draw_route(self, route):
        """Draw the current route on the canvas"""
        self.canvas.delete("all")
        
        # Draw connections between cities
        for i in range(len(route.cities)):
            city_a = route.cities[i]
            city_b = route.cities[(i + 1) % len(route.cities)]
            
            x1, y1 = city_a.x * self.scale + 60, city_a.y * self.scale + 60
            x2, y2 = city_b.x * self.scale + 60, city_b.y * self.scale + 60
            
            # Draw connection line
            self.canvas.create_line(x1, y1, x2, y2, fill="blue", arrow=tk.LAST)
            
        # Draw cities and labels
        for city in route.cities:
            x, y = city.x * self.scale + 60, city.y * self.scale + 60
            
            # Draw city point
            self.canvas.create_oval(x-5, y-5, x+5, y+5, fill="red")
            
            # Draw city label
            self.canvas.create_text(x + 10, y + 6, text=str(city.ID), fill="black")
            
    def update_progress(self, progress_info):
        """Update the visualization with new progress information"""
        current_route = progress_info['current_route']
        iteration = progress_info.get('iteration', 0)
        current_distance = current_route.distance
        best_distance = progress_info.get('best_distance', current_distance)
        
        # Update route visualization
        self.draw_route(current_route)
        
        # Update progress metrics
        self.iteration_var.set(f"Iteration: {iteration}")
        self.distance_var.set(f"Current Distance: {current_distance:.2f}")
        self.best_distance_var.set(f"Best Distance: {best_distance:.2f}")
        
        # Update progress graph
        self.iterations.append(iteration)
        self.distances.append(current_distance)
        self.best_distances.append(best_distance)
        
        self.ax.clear()
        self.ax.plot(self.iterations, self.distances, 'b-', label='Current Distance')
        self.ax.plot(self.iterations, self.best_distances, 'r-', label='Best Distance')
        self.ax.set_xlabel('Iteration')
        self.ax.set_ylabel('Distance')
        self.ax.legend()
        self.ax.grid(True)
        self.canvas_plot.draw()
        
        # Update the window
        self.root.update()
        
    def close(self):
        """Close the visualization window"""
        self.root.destroy()
        
def visualize_desktop_ui(route, real_time=True):
    """Create and return a visualization window"""
    window = TSPVisualizerWindow(route)
    if not real_time:
        window.root.mainloop()
    return window