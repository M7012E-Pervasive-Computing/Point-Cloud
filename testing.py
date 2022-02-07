# examples/python/visualization/non_blocking_visualization.py

import open3d as o3d
import numpy as np
import copy

##Generate two random points
randomPoints1 = np.random.rand(2, 3)

pointSet1 = o3d.geometry.PointCloud()

pointSet1.points = o3d.utility.Vector3dVector(randomPoints1)

o3d.visualization.draw_geometries([pointSet1])

##Add more random points
randomPoints2 = np.random.rand(5, 3)

pointSet2 = o3d.geometry.PointCloud()

pointSet2.points = o3d.utility.Vector3dVector(randomPoints2)