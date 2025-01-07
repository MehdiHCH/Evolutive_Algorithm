from abc import ABC, abstractmethod
from typing import List, Callable
from core.models.route import Route

class TSPAlgorithm(ABC):
    """Base class for TSP optimization algorithms"""
    
    def __init__(self, progress_callback: Callable = None):
        self.progress_callback = progress_callback
        self.iteration = 0
        
    @abstractmethod
    def optimize(self, initial_route: Route) -> Route:
        """Implement the optimization algorithm"""
        pass
    
    def update_progress(self, current_route: Route, **kwargs):
        """Update progress through callback"""
        if self.progress_callback:
            self.iteration += 1
            self.progress_callback(
                iteration=self.iteration,
                current_route=current_route,
                **kwargs
            )