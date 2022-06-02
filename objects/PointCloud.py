import open3d as o3d
import numpy as np

class PointCloud():
    
    def __init__(self, points: np.array or list, debug: bool) -> None:
        self.point_cloud = o3d.geometry.PointCloud()
        self.point_cloud.points = o3d.utility.Vector3dVector(points)
        self.debug = debug
        self.normals()

    def normals(self, radius=0.1, max_nn=30) -> None:
        self.point_cloud.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=radius, max_nn=max_nn))
        if self.debug:
            print("Successfully estimated point cloud normals")

    def set(self, point_cloud: o3d.geometry.PointCloud) -> None:
        self.point_cloud = point_cloud
        self.normals()
        if self.debug:
            print("Successfully updated point cloud")

    def set_points(self, points) -> None:
        print(type(points))
        if isinstance(points, (np.ndarray, np.generic)) or isinstance(points, list):
            print('is numpy array')
            # self.point_cloud.set_points(o3d.utility.Vector3dVector(self.points))
            # type(points) is np.ndarray or type(points) is list:
            self.point_cloud.points = o3d.utility.Vector3dVector(points)
        else:
            print('is not numpy array')
            self.point_cloud.points = points
        self.normals()
        if self.debug:
            print("Successfully updated point cloud points")

    def get(self) -> o3d.geometry.PointCloud:
        return self.point_cloud

    def get_points(self) -> np.array:
        return np.asarray(self.point_cloud.points)
        
    
    