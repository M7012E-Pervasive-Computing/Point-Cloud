
import open3d as o3d

class DenoiseOutlier():
        
    @staticmethod
    def statistical_outlier(point_cloud, ratio, neighbors):    
        _, index = point_cloud.remove_statistical_outlier(nb_neighbors=neighbors, std_ratio=ratio, print_progress=False)
        
        inliers = point_cloud.select_by_index(index)
        inliers.paint_uniform_color([0, 0, 1])
        outlier = point_cloud.select_by_index(index, invert=True)
        outlier.paint_uniform_color([1, 0, 0])
        o3d.visualization.draw_geometries([inliers, outlier])
        
        inliers.paint_uniform_color([0, 0, 0])
        return inliers
    
    @staticmethod
    def radius_outlier(point_cloud, radius, neighbors):    
        _, index = point_cloud.remove_radius_outlier(nb_points=neighbors, radius=radius, print_progress=False)

        inliers = point_cloud.select_by_index(index)
        inliers.paint_uniform_color([0, 0, 1])
        outlier = point_cloud.select_by_index(index, invert=True)
        outlier.paint_uniform_color([1, 0, 0])
        o3d.visualization.draw_geometries([inliers, outlier])
        
        inliers.paint_uniform_color([0, 0, 0])
        return inliers