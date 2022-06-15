import open3d as o3d

class Downsampling():
    
    @staticmethod
    def voxel_down(point_cloud: o3d.geometry.PointCloud, voxel_size: float) -> o3d.geometry.PointCloud:
        """Voxel down a point cloud.

        Args:
            point_cloud (o3d.geometry.PointCloud): point cloud to voxel down. 
            voxel_size (float): voxel size to use. 

        Returns:
            o3d.geometry.PointCloud: Voxel down point cloud.
        """
        return point_cloud.voxel_down_sample(voxel_size=voxel_size)