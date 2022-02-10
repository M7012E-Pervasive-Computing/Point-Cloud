# examples/python/visualization/non_blocking_visualization.py

from time import sleep
from open3d import geometry, utility, visualization as o3d
import numpy as np

class PointCloud2:

    def __init__(self, plotting=np.empty((0,3)), pointSet=geometry.PointCloud(), window=utility.Vector3dVector()):
        self.plotting = plotting
        self.pointSet = pointSet
        self.vis = o3d.visualization.Visualizer()
        self.window=self.vis.create_window()

    def add_data(self, data):
        self.vis.update_geometry(data)
        self.vis.poll_events()
        self.vis.update_renderer()

    def your_update_function(self):
        #Your update routine
        self.vis.update_geometry(cloud)
        self.vis.update_renderer()
        self.vis.poll_events()
        self.vis.run()   

    # def plot_data(self):
    #     self.pointSet.points = utility.Vector3dVector()
    #     visualization.draw_geometries([self.pointSet])

# Pass xyz to Open3D.o3d.geometry.PointCloud and visualize
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(xyz)
    o3d.io.write_point_cloud("../../TestData/sync.ply", pcd)

obj = PointCloud2()

while(True):
    obj.add_data(np.random.rand(50,3))

    