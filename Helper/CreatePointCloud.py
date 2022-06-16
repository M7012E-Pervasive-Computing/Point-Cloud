import open3d as o3d

class CreatePointCloud():
    
    @staticmethod
    def open3d(points: list, debug=False) -> o3d.geometry.PointCloud:
        """Create a open3d point cloud.

        Args:
            points (list): All points as [x, y, z].
            debug (bool, optional): For debug visualization. Defaults to False.

        Returns:
            o3d.geometry.PointCloud: Point cloud.
        """
        point_cloud = o3d.geometry.PointCloud()
        point_cloud.points = o3d.utility.Vector3dVector(points)
        point_cloud.paint_uniform_color([0, 0, 0])
        if debug:
            o3d.visualization.draw_geometries([point_cloud])
        return point_cloud
