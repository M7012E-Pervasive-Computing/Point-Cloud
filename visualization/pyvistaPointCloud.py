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
        
        self.points = self.point_cloud.get_points()
        
        # Create point cloud
        point_cloud = pv.PolyData(self.points)
        np.allclose(self.points, point_cloud.points)
        data = self.points[:,-1] # Make data array using z-component of points array
        point_cloud["elevation"] = data
        point_cloud.plot(render_points_as_spheres=True)
        
        # Surface reconstruction 
        # points = pv.wrap(point_cloud.points)
        # print(points)
        # surf = points.reconstruct_surface()
        # pl = pv.Plotter(shape=(1, 2))
        # pl.add_mesh(points, color=True)
        # pl.add_title('Point Cloud of 3D Surface')
        # pl.subplot(0, 1)
        # pl.add_mesh(surf, color=True, show_edges=True)
        # pl.add_title('Reconstructed Surface')
        # pl.show()
        
        
        # # Create volyme
        # volume = point_cloud.delaunay_3d(alpha=2.)
        # shell = volume.extract_geometry()
        # shell.plot()
        
        
        

