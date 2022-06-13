from open3d import utility, visualization, geometry

from objects.PointCloud import PointCloud 
from visualization.vizPointCloud import VisualizationPointCloud
        
class Open3DPointCloud(VisualizationPointCloud):
    """
    Class for plotting point clouds using open3D
    http://www.open3d.org/docs/release/tutorial/visualization/non_blocking_visualization.html
    """
    
    def __init__(self, point_cloud: list, width=480, height=480):
        super().__init__('OPEN3D', point_cloud)
        self.width = width
        self.height = height

    def visualize(self): 
        super().visualize()
        
        # Create visualizer
        vis = visualization.Visualizer()
        vis.create_window(width=self.width, height=self.height)
        vis.add_geometry(self.point_cloud.get())
        vis.poll_events()
        vis.update_renderer()
        
        # Run interactive window of visualizer
        vis.run()
        