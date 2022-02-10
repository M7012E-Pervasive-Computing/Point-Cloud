# examples/python/visualization/non_blocking_visualization.py

from time import sleep
from open3d import geometry, utility, visualization
import numpy as np

class PointCloud:

    def __init__(self, plotting=np.empty((0,3)), pointSet=geometry.PointCloud()):
        self.plotting = plotting
        self.pointSet = pointSet

    def add_data(self, data):
        self.plotting=np.concatenate((self.plotting,data))
        print(self.plotting)
        

    def plot_data(self):
        self.pointSet.points = utility.Vector3dVector(self.plotting)
        visualization.draw_geometries([self.pointSet])


obj = PointCloud()

while(True):
    obj.add_data(np.random.rand(50,3))
    obj.plot_data()

    