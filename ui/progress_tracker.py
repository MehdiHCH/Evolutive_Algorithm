from typing import Optional
from tqdm import tqdm
from ui.desktop_ui import visualize_desktop_ui
from ui.web_ui import launch_web_ui
from ui.console_ui import visualize_console_ui

class ProgressTracker:
    """Handles progress updates for different UI types with TQDM progress bar"""
    
    def __init__(self, ui_type: str, total_iterations: Optional[int] = None):
        """
        Initialize the progress tracker.
        
        Args:
            ui_type: Type of UI ('desktop', 'web', or 'console')
            total_iterations: Total number of iterations expected (for progress bar)
        """
        self.ui_type = ui_type
        self.desktop_window = None
        self.web_socket = None
        self.total_iterations = total_iterations
        self.progress_bar = None
        self.best_distance = float('inf')
        
        # Initialize progress bar if total iterations is known
        if total_iterations and ui_type == "console":
            self.progress_bar = tqdm(
                total=total_iterations,
                desc="Optimizing route",
                unit="iterations",
                bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} "
                          "[{elapsed}<{remaining}, {rate_fmt}]"
            )
    
    def __call__(self, **progress_info):
        """
        Update progress information.
        
        Args:
            progress_info: Dictionary containing progress information
                Required keys:
                - current_route: Current Route object
                - iteration: Current iteration number
                Optional keys:
                - temperature: Current temperature (for SA)
                - population_size: Current population size (for GA)
                - mutation_rate: Current mutation rate
                - best_distance: Best distance found so far
        """
        # Update best distance if provided
        if 'best_distance' in progress_info:
            self.best_distance = min(self.best_distance, progress_info['best_distance'])
        
        # Update UI based on type
        if self.ui_type == "desktop":
            self._update_desktop(**progress_info)
            return self.desktop_window
        elif self.ui_type == "web":
            self._update_web(**progress_info)
        elif self.ui_type == "console":
            self._update_console(**progress_info)
    
    def _update_desktop(self, **progress_info):
        """Update desktop UI with current progress"""
        if not self.desktop_window:
            self.desktop_window = visualize_desktop_ui(
                progress_info['current_route'],
                real_time=True
            )
        else:
            self.desktop_window.update_progress(progress_info)
    
    def _update_web(self, **progress_info):
        """Update web UI with current progress"""
        if not self.web_socket:
            self.web_socket = launch_web_ui(
                progress_info['current_route'],
                real_time=True
            )
        else:
            self.web_socket.send_update(progress_info)
    
    def _update_console(self, **progress_info):
        """Update console UI with current progress and progress bar"""
        current_route = progress_info['current_route']
        iteration = progress_info.get('iteration', 0)
        
        # Update progress bar if it exists
        if self.progress_bar:
            # Update progress
            self.progress_bar.n = iteration
            
            # Update description with current distances
            desc = f"Current: {current_route.distance:.2f}, Best: {self.best_distance:.2f}"
            
            # Add algorithm-specific information
            if 'temperature' in progress_info:
                desc += f", Temp: {progress_info['temperature']:.2f}"
            if 'population_size' in progress_info:
                desc += f", Pop: {progress_info['population_size']}"
            if 'mutation_rate' in progress_info:
                desc += f", Mut: {progress_info['mutation_rate']:.3f}"
            
            self.progress_bar.set_description(desc)
            self.progress_bar.refresh()
        
        # Regular console updates for non-progress bar mode
        elif iteration % 100 == 0:
            visualize_console_ui(current_route)
            print(
                f"\rItération {iteration}: "
                f"Distance = {current_route.distance:.2f}, "
                f"Meilleure = {self.best_distance:.2f}",
                end=""
            )
    
    def close(self):
        """Clean up resources"""
        if self.progress_bar:
            self.progress_bar.close()
        if self.desktop_window:
            self.desktop_window.close()
        if self.web_socket:
            self.web_socket.close()