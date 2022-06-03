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
                pcd.cluster_dbscan(eps=0.2, min_points=10, print_progress=self.plot))

        max_label = np.max(labels)
        print(f"point cloud has {max_label + 1} clusters")

        colors = plt.get_cmap("tab20")(labels / (max_label if max_label > 0 else 1))
        colors[labels < 0] = 0
        pcd.colors = o3d.utility.Vector3dVector(colors[:, :3])

        sorted_arr = self.sort_on_labels(pcd)
        
        if (self.plot):
            o3d.visualization.draw_geometries([pcd],
                                        zoom=0.455,
                                        front=[-0.4999, -0.1659, -0.8499],
                                        lookat=[2.1813, 2.0619, 2.0999],
                                        up=[0.1204, -0.9852, 0.1215])
        import pyvista as pv
        # sorted_arr.pop(1)
        # sorted_arr.pop(2)
        return_arr = []
        for element in sorted_arr:
            new_point_cloud = PointCloud(element, False) 
            if len(new_point_cloud.get_points()) > 30:
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