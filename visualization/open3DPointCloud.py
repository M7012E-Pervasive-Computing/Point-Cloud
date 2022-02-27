from open3d import utility, visualization, geometry
import numpy as np
import requests
import json

from visualization.vizPointCloud import VisualizationPointCloud

# class PointHandler:
#     def __init__(self) -> None:
#         utility.set_verbosity_level(utility.VerbosityLevel.Info)
        
#         p = requests.get('http://130.240.202.87:3000/Johans%20livingroom')
#         p = json.loads(p.text)
        
#         self.points = np.array([[p[i]["x"]/10, p[i]["y"]/10, p[i]["z"]/10] for i in range(len(p))])
#         self.point_cloud = geometry.PointCloud()
#         self.point_cloud.points = utility.Vector3dVector(self.points)
        
        
#         self.vis = visualization.Visualizer()
#         self.vis.create_window(width=480, height=480)
#         self.vis.add_geometry(self.point_cloud)
            
#         self.point_cloud.points = utility.Vector3dVector(self.points)
#         self.vis.update_geometry(self.point_cloud)
#         self.vis.poll_events()
#         self.vis.update_renderer()
            
#         self.vis.run()
        
# p = PointHandler()
        
class Open3DPointCloud(VisualizationPointCloud):
    
    def __init__(self, points: list, width=480, height=480):
        super().__init__('OPEN3D', points)
        self.width = width
        self.height = height
        
    def visualize(self):         
        point_cloud = geometry.PointCloud()
        point_cloud.points = utility.Vector3dVector(self.points)
        
        vis = visualization.Visualizer()
        vis.create_window(width=self.width, height=self.height)
        vis.add_geometry(point_cloud)
        
        self.point_cloud.points = utility.Vector3dVector(self.points)
        vis.update_geometry(point_cloud)
        vis.poll_events()
        vis.update_renderer()
        
        vis.run()
    
Open3DPointCloud([{"x": 0, "y": 0, "z": 0}, {"x": 1, "y": 0, "z": 0}, {"x": 0, "y": 1, "z": 0}])
        
    
        

