from dis import dis
# from operator import invert
# from turtle import distance
import open3d as o3d
# import pyvista as pv
import numpy as np
from numpy import linalg as npl
# import copy
import matplotlib.pyplot as plt
from math import atan2, degrees, pi
# from rdp import rdp


class Test():
    def __init__(self, points) -> None:
        self.pcd = o3d.geometry.PointCloud()
        self.pcd.points = o3d.utility.Vector3dVector(points)
        self.pcd.paint_uniform_color([0, 0, 0])
        
        self.test3()

    # TODO 1. allow connectLines to create multiple lines instead of force connect into one, should have distance threshold.
    # TODO 2. slice for height and link layers
    # TODO 3. add shape to obj 
    # TODO 4. maybe add an optimizing  for angles of 90 degrees, so that it attempts to push points for lines so that they form better angles.
    # TODO 5. work on parameters (as much as possible to be generalized instead of selective)
    
    def test3(self):
        pcd = self.denoise(self.pcd, ratio=0.05, neighbors=75)
        vox = self.voxel_down(pcd=pcd, voxel_size=0.5)
        pcd2 = self.denoise(pcd=vox, ratio=0.05, neighbors=25)
        
        clust = self.clustering(pcd=pcd2, eps=0.8, min_points=75)
        
        lines = self.getLines(clust) 
        line = self.connectLines(lines) 
        simplified_line = self.rdp_angle(line, dist_threshold=1, angle_divider=2)
        
        x = [x for x, _ in simplified_line]
        y = [y for _, y in simplified_line]
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
        
    def clustering(self, pcd, eps, min_points):
        def sort_on_labels(pcd):
            all_colors = []
            pcd_colors = np.asarray(pcd.colors)
            pcd_arr = np.asarray(pcd.points)
            return_array = []
            rest_array = []
            for color in pcd_colors:
                if (not is_in(color, all_colors)):
                    all_colors.append(color)
            for color in all_colors:
                temp_arr = []
                for index in range(len(pcd_colors)):
                    if ((color == pcd_colors[index]).all()):
                        temp_arr.append(pcd_arr[index])
                if (is_black(color)):
                    rest_array.extend(temp_arr)
                else:
                    return_array.append(temp_arr)
            return return_array, rest_array
            
        
        def is_in(element, array):
            for ind in array:
                if (element == ind).all():
                    return True
            return False
        
        def is_black(color):
            r, g, b = color
            if r == 0 and g == 0 and b == 0:
                return True
            else:
                return False
        
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
        
        sorted_arr, rest_arr = sort_on_labels(pcd)
        if min_points > 10 and len(rest_arr) > 0:
            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(rest_arr) 
            sorted_rest = self.clustering(pcd, eps, int(round(min_points/2)))
            sorted_arr.extend(sorted_rest)
        return sorted_arr
    
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
    
    def connectLines(self, lines):  #? Add distance threshold parameter
        def distPoints(p1, p2):
            x1, y1 = p1
            x2, y2 = p2
            return np.sqrt((y2-y1)**2 + (x2-x1)**2) 
                
        def sortLongest(lines):
            sorted_lines = []
            while len(lines) > 0:
                longest = -np.inf
                best = None
                for idx, line in enumerate(lines):
                    p1, p2 = line
                    dist = distPoints(p1, p2)
                    if dist > longest:
                        longest = dist
                        best = idx
                sorted_lines.append(lines.pop(best))
            return sorted_lines
                
        lines = sortLongest(lines)  
        points = lines[0]   #? List of points which connect into one line 
        lines.pop(0)
        while len(lines) > 0: 
            p = points[-1]
            bestDist = np.inf
            best = None
            idx = None 
            for i, [p1, p2] in enumerate(lines):    
                dist1 = distPoints(p, p1)   #? Check if the distances are larger then distance threshold
                dist2 = distPoints(p, p2)   #? ^
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
                continue    #? instead of having the current list "points" have a list where one index would be the current "points".
                            #? Then instead of continue we append to that new list.
            else: 
                points.extend(best)
                lines.pop(idx)
        return points
            
    def rdp_angle(self, line, dist_threshold, angle_divider):   # Based on idea of rdp algorithm 
        def points_angle(A, B, C):
            Ax, Ay = A[0]-B[0], A[1]-B[1]
            Cx, Cy = C[0]-B[0], C[1]-B[1]
            a = atan2(Ay, Ax)
            c = atan2(Cy, Cx)
            a += pi*2 if a < 0 else 0 
            c += pi*2 if c < 0 else 0
            angle = (pi*2 + c - a) if a > c else (c - a)
            return degrees(angle)
        
        def point_line_distance(A, B, C):
            return npl.norm(np.cross(C-A, A-B))/npl.norm(C-A)
        
        while True:
            length = len(line) - 1
            
            largestDiff = -np.inf
            idx = None
            for i in range(1, length):
                A = np.array(line[(i-1) % length])
                B = np.array(line[i])
                C = np.array(line[(i+2) % length])
                
                angle = points_angle(A, B, C)
                dist = point_line_distance(A, B, C)            
                dist = (dist / angle_divider) if angle < 70 else dist   # Done since this algorithm will generally struggle with smaller angles
                dist = (dist / angle_divider) if angle < 50 else dist   # To make simplification more accurate
                dist = (dist / angle_divider) if angle < 30 else dist
            
                if dist < dist_threshold: 
                    diff = dist_threshold - dist
                    if diff > largestDiff:
                        largestDiff = diff
                        idx = i
                        
            if idx is None: 
                if len(line) > 0: 
                    line.append(line[0])
                return line
            line.pop(idx)