import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt

class Clustering():

    def __init__(self, points: list):
        self.points = points


    def cluster_data(self):
        # creates a points cloud in open3d
        point_cloud = o3d.geometry.PointCloud()
        point_cloud.points = o3d.utility.Vector3dVector(self.points)
        pcd = point_cloud.voxel_down_sample(voxel_size=0.02)
        with o3d.utility.VerbosityContextManager(
            o3d.utility.VerbosityLevel.Debug) as cm:
            labels = np.array(
                pcd.cluster_dbscan(eps=0.02, min_points=10, print_progress=True))

        max_label = np.max(labels)
        print(f"point cloud has {max_label + 1} clusters")

        colors = plt.get_cmap("tab20")(labels / (max_label if max_label > 0 else 1))
        colors[labels < 0] = 0
        pcd.colors = o3d.utility.Vector3dVector(colors[:, :3])
        o3d.visualization.draw_geometries([pcd],
                                        zoom=0.455,
                                        front=[-0.4999, -0.1659, -0.8499],
                                        lookat=[2.1813, 2.0619, 2.0999],
                                        up=[0.1204, -0.9852, 0.1215])
