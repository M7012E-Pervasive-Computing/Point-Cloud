from ast import While
from open3d import utility, visualization, geometry
import numpy as np
import threading
import time

class PointHandler: 

    def __init__(self) -> None: 
        utility.set_verbosity_level(utility.VerbosityLevel.Info)

        self.points = np.random.rand(0,3)
        self.thread = None 
        self.window = None 
            
    def add_points(self, new_points=np.random.rand(1, 3)) -> None:
        print(len(self.points))    
        self.points = np.concatenate((self.points, new_points))
        point_cloud = geometry.PointCloud()
        point_cloud.points = utility.Vector3dVector(self.points)
        self.new_thread(point_cloud)

    def new_thread(self, point_cloud) -> None: 
        while (self.thread and self.thread.is_alive()):
            time.sleep(1)           
        self.window = self.Window(point_cloud)
        self.thread = threading.Thread(target=self.window.create_window)
        self.thread.start()
        
    class Window:
        def __init__(self, point_cloud) -> None:
            self.vis = visualization.Visualizer()
            self.point_cloud = point_cloud
        
        def create_window(self) -> None:
            self.vis.create_window(width=480, height=480)
            self.vis.add_geometry(self.point_cloud)
            self.vis.update_geometry(self.point_cloud)
            self.vis.poll_events()
            self.vis.update_renderer()
            self.vis.run()


# class PointHandler:
    
#     def __init__(self) -> None:
#         utility.set_verbosity_level(utility.VerbosityLevel.Info)
        
#         self.points = np.random.rand(3, 3)
#         self.point_cloud = geometry.PointCloud()
#         self.point_cloud.points = utility.Vector3dVector(self.points)
        
        
#         self.vis = visualization.Visualizer()
#         self.vis.create_window(width=480, height=480)
#         self.vis.add_geometry(self.point_cloud)
        
#         for i in range(100):
#             input("next?")
#             self.points = np.concatenate((self.points, np.random.rand(1, 3)))
#             self.point_cloud.points = utility.Vector3dVector(self.points)
#             self.vis.update_geometry(self.point_cloud)
#             self.vis.poll_events()
#             self.vis.update_renderer()
        

point_handler = PointHandler()

for i in range(100):
    point_handler.add_points()

