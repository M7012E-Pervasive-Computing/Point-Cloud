
class Downsampling():
    
    @staticmethod
    def voxel_down(point_cloud, voxel_size):
        return point_cloud.voxel_down_sample(voxel_size=voxel_size)