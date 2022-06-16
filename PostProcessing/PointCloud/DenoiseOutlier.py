
import open3d as o3d

class DenoiseOutlier():
        
    @staticmethod
    def statistical_outlier(point_cloud: o3d.geometry.PointCloud, ratio: float, neighbors: int, debug=False) -> o3d.geometry.PointCloud:    
        """Apply statistical outliers on point cloud. 

        Args:
            point_cloud (o3d.geometry.PointCloud): Point cloud.
            ratio (float): Ratio to use.
            neighbors (int): Number of neighbors. 
            debug (bool, optional): Debug visualization. Defaults to False.

        Returns:
            o3d.geometry.PointCloud: Resulting Point Cloud from statistical outliers. 
        """
        _, index = point_cloud.remove_statistical_outlier(
            nb_neighbors=neighbors, 
            std_ratio=ratio, 
            print_progress=False)
        
        inliers = point_cloud.select_by_index(index)
        outlier = point_cloud.select_by_index(index, invert=True)
        
        if debug:
            inliers.paint_uniform_color([0, 0, 1])
            outlier.paint_uniform_color([1, 0, 0])
            o3d.visualization.draw_geometries([inliers, outlier])
        
        inliers.paint_uniform_color([0, 0, 0])
        return inliers
    
    @staticmethod
    def radius_outlier(point_cloud: o3d.geometry.PointCloud, radius: float, neighbors: int, debug=False) -> o3d.geometry.PointCloud:    
        """Apply radius outliers on point cloud. 

        Args:
            point_cloud (o3d.geometry.PointCloud): Point cloud.
            radius (float): Radius to use.
            neighbors (int): Number of neighbors. 
            debug (bool, optional): Debug visualization. Defaults to False.

        Returns:
            o3d.geometry.PointCloud: Resulting Point Cloud from radius outliers. 
        """
        _, index = point_cloud.remove_radius_outlier(
            nb_points=neighbors, 
            radius=radius, 
            print_progress=False)

        inliers = point_cloud.select_by_index(index)
        outlier = point_cloud.select_by_index(index, invert=True)
        
        if debug:
            inliers.paint_uniform_color([0, 0, 1])
            outlier.paint_uniform_color([1, 0, 0])
            o3d.visualization.draw_geometries([inliers, outlier])
        
        inliers.paint_uniform_color([0, 0, 0])
        return inliers