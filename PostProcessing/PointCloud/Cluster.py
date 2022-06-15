
import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt

class Cluster():
    
    @staticmethod
    def clustering(point_cloud, eps, min_points, debug=False):
        labels = np.array(point_cloud.cluster_dbscan(eps=eps, min_points=min_points, print_progress=False))

        max_label = np.max(labels)
        # print(f"point cloud has {max_label + 1} clusters")

        colors = plt.get_cmap("tab20")(labels / (max_label if max_label > 0 else 1))
        colors[labels < 0] = 0
        point_cloud.colors = o3d.utility.Vector3dVector(colors[:, :3])
        
        if debug:
            o3d.visualization.draw_geometries([point_cloud])
        
        sorted_arr, rest_arr = Cluster.__sort_on_labels(point_cloud)
        if min_points > 5 and len(rest_arr) > 0:
            point_cloud = o3d.geometry.PointCloud()
            point_cloud.points = o3d.utility.Vector3dVector(rest_arr) 
            sorted_rest = Cluster.clustering(point_cloud, eps, int(round(min_points/2)))
            sorted_arr.extend(sorted_rest)
        return sorted_arr
    
    @staticmethod
    def __sort_on_labels(point_cloud):
        all_colors = []
        pcd_colors = np.asarray(point_cloud.colors)
        pcd_arr = np.asarray(point_cloud.points)
        clusters = []
        unclustered = []
        for color in pcd_colors:
            if (not Cluster.__is_in(color, all_colors)):
                all_colors.append(color)
        for color in all_colors:
            temp_arr = []
            for index in range(len(pcd_colors)):
                if ((color == pcd_colors[index]).all()):
                    temp_arr.append(pcd_arr[index])
            if (Cluster.__is_black(color)):
                unclustered.extend(temp_arr)
            else:
                clusters.append(temp_arr)
        return clusters, unclustered
    
    @staticmethod
    def __is_in(element, array):
        for ind in array:
            if (element == ind).all():
                return True
        return False
    
    @staticmethod  
    def __is_black(color):
        r, g, b = color
        if r == 0 and g == 0 and b == 0:
            return True
        else:
            return False