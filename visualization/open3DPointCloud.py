from open3d import utility, visualization, geometry
import numpy as np
import requests
import json

from visualization.vizPointCloud import VisualizationPointCloud
        
class Open3DPointCloud(VisualizationPointCloud):
    """
    Class for plotting point clouds using open3D
    http://www.open3d.org/docs/release/tutorial/visualization/non_blocking_visualization.html
    """
    
    def __init__(self, points: list, width=480, height=480):
        super().__init__('OPEN3D', points)
        self.width = width
        self.height = height
        
    def visualize(self): 
        super().visualize()
        
        # Create point cloud
        point_cloud = geometry.PointCloud()
        point_cloud.points = utility.Vector3dVector(self.points)
        
        # Create visualizer
        vis = visualization.Visualizer()
        vis.create_window(width=self.width, height=self.height)
        vis.add_geometry(point_cloud)
        vis.poll_events()
        vis.update_renderer()
        
        # Run interactive window of visualizer
        vis.run()
        
    
        

