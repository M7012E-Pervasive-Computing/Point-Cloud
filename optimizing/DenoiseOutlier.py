from os import remove
import open3d as o3d
import numpy as np

from objects.PointCloud import PointCloud

class DenoiseOutlier():
    
    def __init__(self, point_cloud: PointCloud, debug: bool):
        self.voxel_size = 0.02
        self.point_cloud = point_cloud
        self.voxel_down_pcd = self.point_cloud.get().voxel_down_sample(voxel_size=self.voxel_size)
        self.debug = debug

    def statistical_outlier(self, ratio=0.2, neighbors=10):
        # Get the index for what points to keep
        cl, index = self.voxel_down_pcd.remove_statistical_outlier(nb_neighbors=neighbors,
                                                    std_ratio=ratio, print_progress=True)
        self.get_point_from_index(index)
        if self.debug:
            print(f"Successfully applied statistical outlier with ratio={ratio}, neighbors={neighbors}")
        
    def radius_outlier(self, nb_points=10, radius=0.1):
        # Get the index for what points to keep
        cl, index = self.voxel_down_pcd.remove_radius_outlier(nb_points=nb_points, radius=radius)
        self.get_point_from_index(index)
        if self.debug:
            print(f"Successfully applied radius outlier with nb_points={nb_points}, radius={radius}")

    def get_point_from_index(self, index):
        inlier_cloud = self.voxel_down_pcd.select_by_index(index)
        
        # Create a numpy array from the chosen points
        original_data = self.point_cloud.get_points()
        new_data = np.asarray(inlier_cloud.points)
        
        print(f"Removed', {len(original_data) - len(new_data)} \nPoints left: {len(new_data)}")
        self.point_cloud.set_points(o3d.utility.Vector3dVector(new_data))
        self.voxel_down_pcd = self.point_cloud.get().voxel_down_sample(voxel_size=self.voxel_size)
    
    def get_point_cloud(self):
        return self.point_cloud