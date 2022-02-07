# examples/python/visualization/non_blocking_visualization.py

import open3d as o3d
import numpy as np

class test:

    plotting=np.random.rand(200, 3)
    pointSet= o3d.geometry.PointCloud()

    for i in range(2):
        arr=np.random.rand(200, 3)
        plotting=np.concatenate((plotting,arr))
        print(plotting)
        pointSet.points = o3d.utility.Vector3dVector(plotting)
        o3d.visualization.draw_geometries([pointSet])