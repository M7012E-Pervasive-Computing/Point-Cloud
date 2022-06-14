
import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt

class Clustering():
    
    @staticmethod
    def cluster(point_cloud, eps, min_points):
        with o3d.utility.VerbosityContextManager(
            o3d.utility.VerbosityLevel.Debug) as cm:
            labels = np.array(
                point_cloud.cluster_dbscan(eps=eps, min_points=min_points, print_progress=False))

        max_label = np.max(labels)
        # print(f"point cloud has {max_label + 1} clusters")

        colors = plt.get_cmap("tab20")(labels / (max_label if max_label > 0 else 1))
        colors[labels < 0] = 0
        point_cloud.colors = o3d.utility.Vector3dVector(colors[:, :3])
        
        o3d.visualization.draw_geometries([point_cloud],
                                            zoom=0.8,
                                            front=[-0.4999, -0.1659, -0.8499],
                                            lookat=[2.1813, 2.0619, 2.0999],
                                            up=[0.1204, -0.9852, 0.1215])
        
        sorted_arr, rest_arr = Clustering._sort_on_labels(point_cloud)
        if min_points > 10 and len(rest_arr) > 0:
            point_cloud = o3d.geometry.PointCloud()
            point_cloud.points = o3d.utility.Vector3dVector(rest_arr) 
            sorted_rest = Clustering.cluster(point_cloud, eps, int(round(min_points/2)))
            sorted_arr.extend(sorted_rest)
        return sorted_arr
    
    @staticmethod
    def _sort_on_labels(point_cloud):
        all_colors = []
        pcd_colors = np.asarray(point_cloud.colors)
        pcd_arr = np.asarray(point_cloud.points)
        clusters = []
        unclustered = []
        for color in pcd_colors:
            if (not Clustering._is_in(color, all_colors)):
                all_colors.append(color)
        for color in all_colors:
            temp_arr = []
            for index in range(len(pcd_colors)):
                if ((color == pcd_colors[index]).all()):
                    temp_arr.append(pcd_arr[index])
            if (Clustering._is_black(color)):
                unclustered.extend(temp_arr)
            else:
                clusters.append(temp_arr)
        return clusters, unclustered
    
    @staticmethod
    def _is_in(element, array):
        for ind in array:
            if (element == ind).all():
                return True
        return False
    
    @staticmethod  
    def _is_black(color):
        r, g, b = color
        if r == 0 and g == 0 and b == 0:
            return True
        else:
            return False