from objects.PointCloud import PointCloud

import open3d as o3d
import numpy as np

class Ransac():
    
    def __init__(self, point_cloud: PointCloud, debug: bool):
        self.point_cloud = point_cloud
        self.size = self.point_cloud.get_points()
        
    def apply(self):
        model, inliers = self.point_cloud.get().segment_plane(distance_threshold=0.01,
                                         ransac_n=4,
                                         num_iterations=1000)
        
        if self.debug:
            [a, b, c, d] = model
            print(f"Plane equation: {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0")

        inlier_cloud = self.point_cloud.get().select_by_index(inliers)
        inlier_cloud.paint_uniform_color([1.0, 0, 0])
        outlier_cloud = self.point_cloud.get().select_by_index(inliers, invert=True)
        outlier_cloud.paint_uniform_color([0, 0, 1.0])
        
        print(f"Removed points: {(np.asarray(inlier_cloud.points)).size}")
        print(f"Points left: {(np.asarray(outlier_cloud.points)).size}")
        
        if self.debug:
            o3d.visualization.draw_geometries([inlier_cloud, outlier_cloud],
                                            zoom=0.8,
                                            front=[-0.4999, -0.1659, -0.8499],
                                            lookat=[2.1813, 2.0619, 2.0999],
                                            up=[0.1204, -0.9852, 0.1215])
            
        points = np.asarray(outlier_cloud.points)
        self.point_cloud.set_points(points)
        if (points > (self.size * 0.2)):
            self.apply()
        