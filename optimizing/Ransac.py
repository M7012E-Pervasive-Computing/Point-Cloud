import abc
from objects.PointCloud import PointCloud

import open3d as o3d
import numpy as np

class Ransac():
    
    def __init__(self, point_cloud: PointCloud, debug: bool):
        self.point_cloud = point_cloud
        self.size = len(self.point_cloud.get_points())
        self.debug = debug
        self.distance_threshold = 0.01
        self.planePoints = []
        
    def apply(self):
        model, inliers = self.point_cloud.get().segment_plane(
            distance_threshold=self.distance_threshold,
            ransac_n=4,
            num_iterations=1000)
        
        # if self.debug:
        #     [a, b, c, d] = model
        #     print(f"Plane equation: {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0")

        inlier_cloud = self.point_cloud.get().select_by_index(inliers)
        return PointCloud(np.asarray(inlier_cloud.points), False)
    #     inlier_cloud.paint_uniform_color([1.0, 0, 0])
    #     outlier_cloud = self.point_cloud.get().select_by_index(inliers, invert=True)
    #     outlier_cloud.paint_uniform_color([0, 0, 1.0])
        
    #     print(f"Removed points: {(np.asarray(inlier_cloud.points)).size}")
    #     print(f"Points left: {(np.asarray(outlier_cloud.points)).size}")
        
    #     if self.debug:
    #         o3d.visualization.draw_geometries([inlier_cloud, outlier_cloud],
    #                                         zoom=0.8,
    #                                         front=[-0.4999, -0.1659, -0.8499],
    #                                         lookat=[2.1813, 2.0619, 2.0999],
    #                                         up=[0.1204, -0.9852, 0.1215])
        
    #     p = np.asarray(inlier_cloud.points)
    #     # [[x, y, z]]
    #     allX = []
    #     allY = []
    #     allZ = []
    #     for value in p:
    #         allX.append(value[0])
    #         allY.append(value[1])
    #         allZ.append(value[2])
    #     xyz = [(max(allX), min(allX)), (max(allY), min(allY)), (max(allZ), min(allZ))]
        
    #     # print("XYZ IS: " + str(xyz))
        
    #     indexToAdd = -1
    #     coordinate = None
    #     if (abs(xyz[0][0] - xyz[0][1]) <= self.distance_threshold):
    #         indexToAdd = 0
    #         coordinate = min(xyz[0]) + (xyz[0][0] - xyz[0][1]) / 2
    #         xyz.remove(xyz[0])
    #     elif (abs(xyz[1][0] - xyz[1][1]) <= self.distance_threshold):
    #         indexToAdd = 1
    #         coordinate = min(xyz[1]) + (xyz[1][0] - xyz[1][1]) / 2
    #         xyz.remove(xyz[1])
    #     elif (abs(xyz[2][0] - xyz[2][1]) <= self.distance_threshold):
    #         indexToAdd = 2
    #         coordinate = min(xyz[2]) + (xyz[2][0] - xyz[2][1]) / 2
    #         xyz.remove(xyz[2])
        
    #     planePoints = []
    #     if indexToAdd == 0:
    #         planePoints = [(coordinate, xyz[0][0], xyz[1][0]), (coordinate, xyz[0][0], xyz[1][1]), (coordinate, xyz[0][1], xyz[1][0]), (coordinate, xyz[0][1], xyz[1][1])]
    #     if indexToAdd == 1:
    #         planePoints = [(xyz[0][0], coordinate, xyz[1][0]), (xyz[0][0], coordinate, xyz[1][1]), (xyz[0][1], coordinate, xyz[1][0]), (xyz[0][1], coordinate, xyz[1][1])]
    #     if indexToAdd == 2:
    #         planePoints = [(xyz[0][0], xyz[1][0], coordinate), (xyz[0][0], xyz[1][1], coordinate), (xyz[0][1], xyz[1][0], coordinate), (xyz[0][1], xyz[1][1], coordinate)]
        
    #     # print(f"Plane points: {planePoints}")
    #     self.planePoints.append(planePoints)

    #     points = np.asarray(outlier_cloud.points)
    #     self.point_cloud.set_points(points)
    #     if (len(points) > (self.size * 0.05)):
    #         # self.apply()
    #         print('test')
        
    # def get_plane_data(self):
    #     return self.planePoints