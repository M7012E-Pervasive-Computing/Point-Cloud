import open3d as o3d
import numpy as np

class Optimizing():
    
    def __init__(self, points: list):
        self.points = np.array([[points[i]["x"], points[i]["y"], points[i]["z"]] for i in range(len(points))])

    def optimize_data(self, ratio=0.5, neighbors=20):
        # creates a points cloud in open3d
        point_cloud = o3d.geometry.PointCloud()
        point_cloud.points = o3d.utility.Vector3dVector(self.points)
        voxel_down_pcd = point_cloud.voxel_down_sample(voxel_size=0.02)
        
        # get the index for what points to keep
        cl, ind = voxel_down_pcd.remove_statistical_outlier(nb_neighbors=neighbors,
                                                    std_ratio=ratio, print_progress=True)
        # only gives the specific points by index
        inlier_cloud = voxel_down_pcd.select_by_index(ind)
        # create a numpy array from the chosen points
        removed_data = np.asarray(inlier_cloud.points)
        
        # restore data to original shape
        data = []
        print('removed', len(self.points) - len(removed_data))
        for i in range(len(removed_data)):
            data.append({"x": removed_data[i][0], "y": removed_data[i][1], "z": removed_data[i][2]})

        # return data
        return data