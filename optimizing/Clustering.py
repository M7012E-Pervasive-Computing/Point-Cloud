from objects.PointCloud import PointCloud
import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt

class Clustering():

    def __init__(self, point_cloud: PointCloud, plot: bool = False):
        self.point_cloud = point_cloud
        self.plot = plot



    def cluster_data(self):
        point_cloud = self.point_cloud.get()
        
        
        pcd = point_cloud.voxel_down_sample(voxel_size=0.02)
        with o3d.utility.VerbosityContextManager(
            o3d.utility.VerbosityLevel.Debug) as cm:
            labels = np.array(
                pcd.cluster_dbscan(eps=0.13, min_points=10, print_progress=True))

        max_label = np.max(labels)
        print(f"point cloud has {max_label + 1} clusters")

        colors = plt.get_cmap("tab20")(labels / (max_label if max_label > 0 else 1))
        colors[labels < 0] = 0
        pcd.colors = o3d.utility.Vector3dVector(colors[:, :3])

        sorted_arr = self.sort_on_labels(pcd)
        
        return_arr = []
        for element in sorted_arr:
            new_point_cloud = PointCloud(element, False)
            return_arr.append(new_point_cloud)
        return return_arr
    
    
    def sort_on_labels(self, pcd):
        all_colors = []
        pcd_colors = np.asarray(pcd.colors)
        pcd_arr = np.asarray(pcd.points)
        return_array = []
        for color in pcd_colors:
            if (not self.is_in(color, all_colors)):
                all_colors.append(color)
        for color in all_colors:
            temp_arr = []
            for index in range(len(pcd_colors)):
                if ((color == pcd_colors[index]).any()):
                    temp_arr.append(pcd_arr[index])
            return_array.append(temp_arr)
        return return_array

    def is_in(self, element, array):
        for ind in array:
            if (element == ind).all():
                return True
        return False