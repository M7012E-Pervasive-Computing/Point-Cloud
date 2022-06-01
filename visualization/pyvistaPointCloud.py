import numpy as np
import pyvista as pv

from objects.PointCloud import PointCloud 
from visualization.vizPointCloud import VisualizationPointCloud

class PyvistaPointCloud(VisualizationPointCloud):
    """
    Class which plots using pyvista
    https://docs.pyvista.org/examples/00-load/create-point-cloud.html
    """
    
    def __init__(self, point_cloud: PointCloud):
        super().__init__('PYVISTA', point_cloud)
        
    def visualize(self):
        super().visualize()
        
        # Create point cloud
        point_cloud = pv.PolyData(self.point_cloud.get_points())
        np.allclose(self.points, point_cloud.points)

        # Make data array using z-component of points array
        data = self.points[:,-1]

        # Add that data to the mesh with the name "uniform dist"
        point_cloud["elevation"] = data

        # Plot the points as spheres
        point_cloud.plot(render_points_as_spheres=True)
        
