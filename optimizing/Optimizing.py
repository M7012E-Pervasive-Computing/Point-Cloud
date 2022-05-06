from os import remove
import open3d as o3d
import numpy as np

class Optimizing():
    
    def __init__(self, points: np.array):
        self.points = points
        
        # insatiate open3d
        self.point_cloud = o3d.geometry.PointCloud()
        self.point_cloud.points = o3d.utility.Vector3dVector(self.points)
        self.voxel_down_pcd = self.point_cloud.voxel_down_sample(voxel_size=0.02)

    def statistical_outlier(self, ratio=0.2, neighbors=10):
        # get the index for what points to keep
        cl, index = self.voxel_down_pcd.remove_statistical_outlier(nb_neighbors=neighbors,
                                                    std_ratio=ratio, print_progress=True)
        
        
        self.get_point_from_index(index)
        
    def radius_outlier(self, nb_points=10, radius=0.1):
        cl, index = self.voxel_down_pcd.remove_radius_outlier(nb_points=nb_points, radius=radius)
        
        self.get_point_from_index(index)

    def get_point_from_index(self, index):
        # only gives the specific points by index
        inlier_cloud = self.voxel_down_pcd.select_by_index(index)
        # create a numpy array from the chosen points
        removed_data = np.asarray(inlier_cloud.points)
        
        # restore data to original shape
        print('Removed', str(len(self.points) - len(removed_data)), '\nPoints left: ' + str(len(removed_data)))

        self.points = removed_data
        self.point_cloud.points = o3d.utility.Vector3dVector(self.points)
    
    def get_points(self):
        return self.points