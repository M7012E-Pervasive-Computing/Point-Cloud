import open3d as o3d
import pyvista as pv
import numpy as np
import matplotlib.pyplot as plt


class Test():
    def __init__(self, points) -> None:
        self.pcd = o3d.geometry.PointCloud()
        self.pcd.points = o3d.utility.Vector3dVector(points)
        self.pcd.paint_uniform_color([0, 0, 0])
        
        self.normals()
        
        self.denoise()
        
        self.ransac_multiple_detection()
        
        self.ransac_euclidean_clustering()
         
    def normals(self, radius=0.1, max_nn=16):
        self.pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=radius, max_nn=max_nn), fast_normal_computation=True)
        
        # Visualize 
        o3d.visualization.draw_geometries([self.pcd])
    
    def denoise(self, voxel_size=0.02, ratio=0.2, neighbors=10):
        inliers = self.pcd.voxel_down_sample(voxel_size=voxel_size)
        _, index = inliers.remove_statistical_outlier(nb_neighbors=neighbors, std_ratio=ratio, print_progress=True)
        
        # Visualize, Removed points are Red and left once are Blue
        inliers = inliers.select_by_index(index)
        inliers.paint_uniform_color([0, 0, 1])
        outlier = self.pcd.select_by_index(index, invert=True)
        outlier.paint_uniform_color([1, 0, 0])
        o3d.visualization.draw_geometries([inliers, outlier])
        
        inliers.paint_uniform_color([0, 0, 0])
        self.pcd = inliers
        
    def ransac_multiple_detection(self, distance_threshold=0.01, ransac_n=4, num_iterations=1000):
        segment_models={}
        segments={}
        max_plane_idx=10
        rest=self.pcd
        for i in range(max_plane_idx):
            colors = plt.get_cmap("tab20")(i)
            segment_models[i], inliers = rest.segment_plane(distance_threshold=distance_threshold,ransac_n=ransac_n,num_iterations=num_iterations)
            segments[i]=rest.select_by_index(inliers)
            segments[i].paint_uniform_color(list(colors[:3]))
            rest = rest.select_by_index(inliers, invert=True)
            # print("pass",i,"/",max_plane_idx,"done.")
            
        # Visualize
        o3d.visualization.draw_geometries([segments[i] for i in range(max_plane_idx)]+[rest])
        
    def ransac_euclidean_clustering(self, distance_threshold=0.01, ransac_n=4, num_iterations=1000, min_points=10):
        segment_models={}
        segments={}
        max_plane_idx=20
        rest=self.pcd
        for i in range(max_plane_idx):
            colors = plt.get_cmap("tab20")(i)
            segment_models[i], inliers = rest.segment_plane(distance_threshold=distance_threshold,ransac_n=ransac_n,num_iterations=num_iterations)
            segments[i]=rest.select_by_index(inliers)
            labels = np.array(segments[i].cluster_dbscan(eps=distance_threshold*10, min_points=min_points))
            candidates=[len(np.where(labels==j)[0]) for j in np.unique(labels)]
            best_candidate=int(np.unique(labels)[np.where(candidates==np.max(candidates))[0]])
            # print("the best candidate is: ", best_candidate)
            rest = rest.select_by_index(inliers, invert=True)+segments[i].select_by_index(list(np.where(labels!=best_candidate)[0]))
            segments[i]=segments[i].select_by_index(list(np.where(labels==best_candidate)[0]))
            segments[i].paint_uniform_color(list(colors[:3]))
            # print("pass",i+1,"/",max_plane_idx,"done.")
            
        # Visualize
        o3d.visualization.draw_geometries([segments[i] for i in range(max_plane_idx)]+[rest])