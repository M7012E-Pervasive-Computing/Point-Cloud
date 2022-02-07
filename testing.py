# examples/python/visualization/non_blocking_visualization.py

from time import sleep
import open3d as o3d
import numpy as np
import copy

class test:

    plotting=np.random.rand(200, 3)
    pointSet= o3d.geometry.PointCloud()

    for i in range(2):
        arr=np.random.rand(200, 3)
        plotting=np.concatenate((plotting,arr))
        print(plotting)
        pointSet.points = o3d.utility.Vector3dVector(plotting)
        o3d.visualization.draw_geometries([pointSet])