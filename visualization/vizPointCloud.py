
import numpy as np

class VisualizationPointCloud: 
    
    def __init__(self, name: str, points: list) -> None:
        self._name = name; 
        self.points = np.array([[points[i]["x"], points[i]["y"], points[i]["z"]] for i in range(len(points))])
        
    
    def get_name(self) -> str: 
        return self._name
    
    
    def visualize(self): 
        pass
    