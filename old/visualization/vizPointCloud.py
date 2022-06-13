from objects.PointCloud import PointCloud

import numpy as np

class VisualizationPointCloud: 
    
    def __init__(self, name: str, point_cloud: PointCloud) -> None:
        self._name = name; 
        self.point_cloud = point_cloud
        
    
    def get_name(self) -> str: 
        return self._name
    
    
    def visualize(self): 
        print(f"[{self.get_name()}] Visualizing")
    