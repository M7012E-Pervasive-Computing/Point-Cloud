
import numpy as np

class VisualizationPointCloud: 
    
    def __init__(self, name: str, points: list) -> None:
        self._name = name; 
        self.points = points
        
    
    def get_name(self) -> str: 
        return self._name
    
    
    def visualize(self): 
        print('[' + self.get_name() +'] Visualizing')
    