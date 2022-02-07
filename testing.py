# examples/python/visualization/non_blocking_visualization.py

from time import sleep
from open3d import geometry, utility, visualization
import numpy as np

class test:

    plotting=np.random.rand(200, 3)
    pointSet= geometry.PointCloud()

    for i in range(2):
        arr=np.random.rand(200, 3)
        plotting=np.concatenate((plotting,arr))
        print(plotting)
        pointSet.points = utility.Vector3dVector(plotting)
        visualization.draw_geometries([pointSet])