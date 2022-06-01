import open3d as o3d
import numpy as np 

class EstimateNormals():
    
    def __init__(self, points: np.array):
        self.points = points
        
    