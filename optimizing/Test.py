from dis import dis
from operator import invert
from turtle import distance
import open3d as o3d
import pyvista as pv
import numpy as np
from numpy import linalg as npl
import copy
import matplotlib.pyplot as plt
from rdp import rdp

from optimizing.Clustering import Clustering


class Test():
    def __init__(self, points) -> None:
        self.pcd = o3d.geometry.PointCloud()
        self.pcd.points = o3d.utility.Vector3dVector(points)
        self.pcd.paint_uniform_color([0, 0, 0])
        
        self.test3()
        
        # self.normals()
        
        # self.denoise()
         
    # def normals(self, radius=0.1, max_nn=16):
    #     self.pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=radius, max_nn=max_nn), fast_normal_computation=True)
        
    #     # Visualize 
    #     o3d.visualization.draw_geometries([self.pcd])
    
    # def denoise(self, voxel_size=0.3, ratio=0.3, neighbors=10):
    #     inliers = self.pcd.voxel_down_sample(voxel_size=voxel_size)
    #     _, index = inliers.remove_statistical_outlier(nb_neighbors=neighbors, std_ratio=ratio, print_progress=True)
        
    #     # Visualize, Removed points are Red and left once are Blue
    #     inliers = inliers.select_by_index(index)
    #     inliers.paint_uniform_color([0, 0, 1])
    #     outlier = self.pcd.select_by_index(index, invert=True)
    #     outlier.paint_uniform_color([1, 0, 0])
    #     o3d.visualization.draw_geometries([inliers, outlier])
        
    #     inliers.paint_uniform_color([0, 0, 0])
    #     self.pcd = inliers
        
    # def ransac_multiple_detection(self, distance_threshold=0.01, ransac_n=4, num_iterations=1000):
    #     segment_models={}
    #     segments={}
    #     max_plane_idx=10
    #     rest=self.pcd
    #     for i in range(max_plane_idx):
    #         colors = plt.get_cmap("tab20")(i)
    #         segment_models[i], inliers = rest.segment_plane(distance_threshold=distance_threshold,ransac_n=ransac_n,num_iterations=num_iterations)
    #         segments[i]=rest.select_by_index(inliers)
    #         segments[i].paint_uniform_color(list(colors[:3]))
    #         rest = rest.select_by_index(inliers, invert=True)
    #         # print("pass",i,"/",max_plane_idx,"done.")
            
    #     # Visualize
    #     o3d.visualization.draw_geometries([segments[i] for i in range(max_plane_idx)]+[rest])
        
    # def ransac_euclidean_clustering(self, distance_threshold=0.01, ransac_n=4, num_iterations=1000, min_points=10):
    #     segment_models={}
    #     segments={}
    #     max_plane_idx=20
    #     rest=self.pcd
    #     for i in range(max_plane_idx):
    #         colors = plt.get_cmap("tab20")(i)
    #         segment_models[i], inliers = rest.segment_plane(distance_threshold=distance_threshold,ransac_n=ransac_n,num_iterations=num_iterations)
    #         segments[i]=rest.select_by_index(inliers)
    #         labels = np.array(segments[i].cluster_dbscan(eps=distance_threshold*10, min_points=min_points))
    #         candidates=[len(np.where(labels==j)[0]) for j in np.unique(labels)]
    #         best_candidate=int(np.unique(labels)[np.where(candidates==np.max(candidates))[0]])
    #         # print("the best candidate is: ", best_candidate)
    #         rest = rest.select_by_index(inliers, invert=True)+segments[i].select_by_index(list(np.where(labels!=best_candidate)[0]))
    #         segments[i]=segments[i].select_by_index(list(np.where(labels==best_candidate)[0]))
    #         segments[i].paint_uniform_color(list(colors[:3]))
    #         # print("pass",i+1,"/",max_plane_idx,"done.")
            
    #     # Visualize
    #     o3d.visualization.draw_geometries([segments[i] for i in range(max_plane_idx)]+[rest])
        
    # def removeDuplicates(self, points):
    #     points = points.tolist()
    #     res = []
    #     for p in points: 
    #         if p not in res:
    #             res.append(p)
    #         else:
    #             continue
    #     return np.asarray(res)
        
    # def distancePoints(self, p1, p2): # TODO Maybe change so that we ignore one axis here
    #     [x1, y1, z1] = p1
    #     [x2, y2, z2] = p2
    #     return np.sqrt(((x2-x1)**2) + ((y2-y1)**2) + ((z2-z1)**2))    
    
    # def edgeNeighbors(self):
    #     original_points = (np.asarray(self.pcd.points)).tolist()
    #     points = copy.deepcopy(original_points)
    #     edges = []
    #     next = 0
    #     while len(points) > 0:
    #         p1 = points.pop(next)
    #         best_distance = np.inf
    #         for p2 in points:
    #             dist = self.distancePoints(p1, p2)
    #             if dist < best_distance:
    #                 best_distance = dist
    #                 next = points.index(p2)
    #             else:
    #                 continue
    #         if len(points) > 0:
    #             edges.append([original_points.index(p1), original_points.index(points[next])]) 
    #         else:
    #             edges.append([original_points.index(p1), 0])
    #     return edges
        
    # def serializePoints(self):
    #     edges = self.edgeNeighbors()
    #     points = (np.asarray(self.pcd.points)).tolist()
    #     res = []
    #     for [_from,to] in edges: 
    #         res.append(points[to])
    #     return np.asarray(res)
    
    # def test(self):
    #     _, inliers = self.pcd.segment_plane(distance_threshold=0.01,ransac_n=4,num_iterations=1000)
    #     inlier_pcd = self.pcd.select_by_index(inliers)
    #     o3d.visualization.draw_geometries([inlier_pcd])
    #     points = np.asarray(inlier_pcd.points)
    #     points = self.removeDuplicates(points)
    #     self.pcd.points = o3d.utility.Vector3dVector(points)
    #     points = rdp.rdp(self.serializePoints(), epsilon=0.5)
    #     self.pcd.points = o3d.utility.Vector3dVector(points)
    #     o3d.visualization.draw_geometries([self.pcd])
        
    # def test2(self):
    #     _, inliers = self.pcd.segment_plane(distance_threshold=0.01,ransac_n=4,num_iterations=1000, seed=420)
    #     inlier_pcd = self.pcd.select_by_index(inliers)        
    #     clusters = self.clustering(inlier_pcd)
    #     self.getLines(clusters, np.asarray(inlier_pcd.points))
        
        
    # def getLines(self, clusters, total):
    #     x = [x for x, _, _ in total]
    #     y = [y for _, y, _ in total]
    #     plt.plot(x, y, 'ko')
    #     for points in clusters:
    #         # x_min = np.inf
    #         # x_max = -np.inf
    #         x_val = []
    #         y_val = []
    #         for x, y, _ in points:
    #             # if x < x_min:
    #             #     x_min = x
    #             # elif x > x_max:
    #             #     x_max = x
    #             x_val.append(x)
    #             y_val.append(y)
                
    #         x = np.array(x_val)
    #         y = np.array(y_val)
            
    #         a, b, c = np.polyfit(x,y,2)
            
    #         plt.plot(x, y, 'o')
    #         plt.plot(x, (a*x**2 + b*x + c))
    #     plt.show()
    
    def test3(self):
        ratio = 0.05
        neighbors = 75
        pcd = self.denoise(self.pcd, ratio, neighbors)
        vox = self.voxel_down(pcd, 0.5)
        new_neighbors = int(round((neighbors/3)))
        pcd2 = self.denoise(vox, ratio, new_neighbors)
        new_neighbors = int(round((neighbors/4.5)))
        clust = self.clustering(pcd2, 0.8, new_neighbors)
        lines = self.getLines(clust) 
        polygon = self.connectLines(lines)
        # x = []
        # y = []
        # for line in polygon:
        #     for val_x, val_y in line:
        #         x.append(val_x)
        #         y.append(val_y)
        res = rdp(polygon, epsilon=1)
        res.insert(0, res.pop())
        res = rdp(res, epsilon=1)
        res.append(res[0])
        x = [x for x, _ in res]
        y = [y for _, y in res]
        plt.plot(x,y)
        plt.show()
                
        
    def voxel_down(self, pcd, voxel_size):
        return pcd.voxel_down_sample(voxel_size=voxel_size)       

        
    def denoise(self, pcd, ratio=0.05, neighbors=100):    
        _, index = pcd.remove_statistical_outlier(nb_neighbors=neighbors, std_ratio=ratio, print_progress=True)
        
        # Visualize, Removed points are Red and left once are Blue
        inliers = pcd.select_by_index(index)
        inliers.paint_uniform_color([0, 0, 1])
        outlier = pcd.select_by_index(index, invert=True)
        outlier.paint_uniform_color([1, 0, 0])
        o3d.visualization.draw_geometries([inliers, outlier])
        
        inliers.paint_uniform_color([0, 0, 0])
        return inliers
        
    def clustering(self, pcd, eps=0.4, min_points=50):
        def sort_on_labels(pcd):
            all_colors = []
            pcd_colors = np.asarray(pcd.colors)
            pcd_arr = np.asarray(pcd.points)
            return_array = []
            for color in pcd_colors:
                if (not is_in(color, all_colors)):
                    if check_valid(color):
                        all_colors.append(color)
            for color in all_colors:
                temp_arr = []
                for index in range(len(pcd_colors)):
                    if ((color == pcd_colors[index]).all()):
                        temp_arr.append(pcd_arr[index])
                return_array.append(temp_arr)
            return return_array
            
        
        def is_in(element, array):
            for ind in array:
                if (element == ind).all():
                    return True
            return False
        
        def check_valid(color):
            r, g, b = color
            if r == 0 and g == 0 and b == 0:
                return False
            else:
                return True
        
        with o3d.utility.VerbosityContextManager(
            o3d.utility.VerbosityLevel.Debug) as cm:
            labels = np.array(
                pcd.cluster_dbscan(eps=eps, min_points=min_points, print_progress=False))

        max_label = np.max(labels)
        print(f"point cloud has {max_label + 1} clusters")

        colors = plt.get_cmap("tab20")(labels / (max_label if max_label > 0 else 1))
        colors[labels < 0] = 0
        pcd.colors = o3d.utility.Vector3dVector(colors[:, :3])
        
        o3d.visualization.draw_geometries([pcd],
                                            zoom=0.8,
                                            front=[-0.4999, -0.1659, -0.8499],
                                            lookat=[2.1813, 2.0619, 2.0999],
                                            up=[0.1204, -0.9852, 0.1215])

        return sort_on_labels(pcd)
    
    def getLines(self, clusters):
        lines = []
        for cluster in clusters:
            x, y = [], []
            x1 = np.inf
            x2 = -np.inf
            for val_x, val_y, _ in cluster:
                x.append(val_x)
                y.append(val_y)
                x1 = val_x if val_x < x1 else x1
                x2 = val_x if val_x > x2 else x2
                
            x = np.array(x)
            y = np.array(y)

            a, b = np.polyfit(x,y,1)
            
            y1 = a*x1 + b
            y2 = a*x2 + b
            
            plt.plot(x, y, 'o')
            plt.plot(x, (a*x + b))
            lines.append([[x1, y1], [x2, y2]])
        # plt.show()
        return lines
    
    def connectLines(self, lines):
        def distPoints(p1, p2):
            x1, y1 = p1
            x2, y2 = p2
            return np.sqrt((y2-y1)**2 + (x2-x1)**2) 
                
        points = lines[0]
        lines.pop(0)
        while len(lines) > 0: 
            p = points[-1]
            bestDist = np.inf
            best = None
            idx = None 
            for i, [p1, p2] in enumerate(lines):
                dist1 = distPoints(p, p1)
                dist2 = distPoints(p, p2)
                if dist1 < dist2: 
                    if dist1 < bestDist:
                        bestDist = dist1
                        best = [p1,p2]
                        idx = i
                else:
                    if dist2 < bestDist:
                        bestDist = dist1
                        best = [p2,p1]
                        idx = i 
            if best is None: 
                continue
            else: 
                points.extend(best)
                lines.pop(idx)
        # points.append(points[0])
        return points
            
                
        
        
                    
            
                    
                
                
                
                
                
            
    

        
        
        
                
    
     
            
        
    
        
        
        