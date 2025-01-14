import tkinter as tk

from tkinter import ttk, PhotoImage
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from core.utils import get_scale, spherical_to_cartesian

class TSPVisualizerWindow:
    def __init__(self, route):
        self.canvas_size = (700, 750)
        self.root = tk.Tk()
        self.root.title("TSP Optimization Visualization")
        self.root.geometry("1400x800")
        self.root.state('zoomed')  # Ouvre la fenêtre en plein écran

        self.zoom_in_image = PhotoImage(file="icons/zoom-in.png").subsample(15, 15)
        self.zoom_out_image = PhotoImage(file="icons/zoom-out.png").subsample(15, 15)
        self.reset_view_image = PhotoImage(file="icons/reset.png").subsample(15, 15)

        # Translation offsets
        self.offset_x = self.canvas_size[0] * 0.20
        self.offset_y = self.canvas_size[1] * 0.05

        # Create main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left panel for route visualization
        left_panel = ttk.Frame(main_container)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Buttons for canvas controls
        control_panel = ttk.Frame(left_panel)
        control_panel.pack(fill=tk.X, pady=10)

        # Add buttons with images
        ttk.Button(control_panel, image=self.zoom_in_image, command=self.zoom_in).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_panel, image=self.zoom_out_image, command=self.zoom_out).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_panel, image=self.reset_view_image, command=self.reset_view).pack(side=tk.LEFT, padx=5)

        # Frame for directional buttons
        directional_frame = ttk.Frame(control_panel)
        directional_frame.pack(side=tk.LEFT, padx=20, pady=10)

        # Add directional buttons in a game controller style using grid
        ttk.Button(directional_frame, text="↑", command=self.translate_up).grid(row=0, column=1, padx=5, pady=1)
        ttk.Button(directional_frame, text="←", command=self.translate_left).grid(row=1, column=0, padx=5, pady=1)
        ttk.Button(directional_frame, text="↓", command=self.translate_down).grid(row=2, column=1, padx=5, pady=5)
        ttk.Button(directional_frame, text="→", command=self.translate_right).grid(row=1, column=2, padx=5, pady=1)

        # Route canvas
        self.canvas = tk.Canvas(left_panel, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)

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
        self.padding = 5
        self.min_values = None
        self.max_values = None
        self.scale = self._calculate_scale(route)
        self.original_scale = self.scale

        # Bind resize event
        self.canvas.bind("<Configure>", self.on_resize)

        # Draw initial route
        self.draw_route(route)
        self.route = route

    def _calculate_scale(self, route):
        """Calculate appropriate scale based on city coordinates"""
        if not route:
            return 0.4
        if not route.cities:
            return 0.4

        scale, self.min_values, self.max_values, self.padding = get_scale(
            spherical_coords=map(lambda city: (city.ID, city.x, city.y), route.cities),
            canvas_size=self.canvas_size,
            padding=self.padding
        )

        scale /= 1.1 ** 2

        return scale

    def draw_route(self, route):
        """Draw the current route on the canvas"""
        if not route:
            return
        self.canvas.delete("all")

        # Draw connections between cities
        for i in range(len(route.cities)):
            city_a = route.cities[i]
            city_b = route.cities[(i + 1) % len(route.cities)]

            converted_coords_a = spherical_to_cartesian(
                spherical_coords=(city_a.ID, city_a.x, city_a.y),
                scale=self.scale,
                min_values=self.min_values,
                max_values=self.max_values,
                padding=self.padding
            )

            x1, y1 = converted_coords_a[1:]
            x1 += self.offset_x
            y1 += self.offset_y

            converted_coords_b = spherical_to_cartesian(
                spherical_coords=(city_a.ID, city_b.x, city_b.y),
                scale=self.scale,
                min_values=self.min_values,
                max_values=self.max_values,
                padding=self.padding
            )

            x2, y2 = converted_coords_b[1:]
            x2 += self.offset_x
            y2 += self.offset_y

            # Draw connection line
            self.canvas.create_line(x1, y1, x2, y2, fill="blue", arrow=tk.LAST)

        # Draw cities and labels
        for city in route.cities:
            idx, x, y = spherical_to_cartesian(
                spherical_coords=(city.ID, city.x, city.y),
                scale=self.scale,
                min_values=self.min_values,
                max_values=self.max_values,
                padding=self.padding
            )

            x += self.offset_x
            y += self.offset_y

            # Draw city point
            self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="red")

            # Draw city label
            self.canvas.create_text(x + 10, y + 6, text=str(city.ID), fill="black")

    def on_resize(self, event):
        """Handle canvas resizing"""
        self.canvas_size = (event.width, event.height)
        self.draw_route(self.route)
    
    def zoom_in(self):
        """Zoom in on the canvas"""
        self.scale *= 1.1
        self.draw_route(self.route)
    
    def zoom_out(self):
        """Zoom out on the canvas"""
        self.scale /= 1.1
        self.draw_route(self.route)
    
    def reset_view(self):
        """Reset the canvas view to the original scale"""
        self.scale = self.original_scale
        self.offset_x = self.canvas_size[0]* 0.20
        self.offset_y = self.canvas_size[1]* 0.05
        self.draw_route(self.route)
    
    def translate_up(self):
        """Translate the canvas view upward"""
        self.offset_y -= 10
        self.draw_route(self.route)
    
    def translate_down(self):
        """Translate the canvas view downward"""
        self.offset_y += 10
        self.draw_route(self.route)
    
    def translate_left(self):
        """Translate the canvas view to the left"""
        self.offset_x -= 10
        self.draw_route(self.route)
    
    def translate_right(self):
        """Translate the canvas view to the right"""
        self.offset_x += 10
        self.draw_route(self.route)  
      
    def update_progress(self, progress_info):
        """Update the visualization with new progress information"""
        current_route = progress_info['current_route']
        if current_route is None:
            return
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

        self.route = current_route
        
        # Update the window
        self.root.update()
        
    def close(self):
        """Close the visualization window"""
        self.root.destroy()
        
def visualize_desktop_ui(route, real_time=False, desktop_window=None):
    """Create and return a visualization window"""
    if desktop_window:
        desktop_window.root.mainloop()
    window = TSPVisualizerWindow(route)
    if not real_time:
        window.root.mainloop()
    return window