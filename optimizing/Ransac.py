
import open3d as o3d
import numpy as np

class Ransac():
    
    def __init__(self, points: list):
        self.points = points
        
    def apply(self):
        point_cloud = o3d.geometry.PointCloud()
        point_cloud.points = o3d.utility.Vector3dVector(self.points)
        model, inliers = point_cloud.segment_plane(distance_threshold=0.01,
                                         ransac_n=4,
                                         num_iterations=100000)
        
        [a, b, c, d] = model
        print(f"Plane equation: {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0")

        inlier_cloud = point_cloud.select_by_index(inliers)
        inlier_cloud.paint_uniform_color([0, 0, 1.0])
        outlier_cloud = point_cloud.select_by_index(inliers, invert=True)
        outlier_cloud.paint_uniform_color([1.0, 0, 0])
        
        print("Removed points: " + str((np.asarray(outlier_cloud.points)).size))
        print("Points left: " + str(np.asarray(inlier_cloud.points).size))
        
        o3d.visualization.draw_geometries([inlier_cloud, outlier_cloud],
                                        zoom=0.8,
                                        front=[-0.4999, -0.1659, -0.8499],
                                        lookat=[2.1813, 2.0619, 2.0999],
                                        up=[0.1204, -0.9852, 0.1215])