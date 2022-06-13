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
from optimizing.Store import Store
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
                
        clusters = self.clustering(pcd=pcd2, eps=0.8, min_points=75)
        
        heights = self.cluster_heights(minValue=pcd.get_min_bound()[2], maxValue=pcd.get_max_bound()[2], divider=0.1)
        clusterData = self.sort_clusters_for_height(clusters=clusters, heights=heights)
        
        height_lines = []
        for height_clusters in clusterData:
            lines = self.getLines(np.asarray(height_clusters))
            lines = self.connectLines(lines, distance_threshold=2)
            simplified_lines = [[]]
            for line in lines:
                simplified_line = self.rdp_angle(line, dist_threshold=1.5, angle_multiplier=1.25)
                simplified_lines.append(simplified_line)
            height_lines.append(simplified_lines)
            # plt.show()
        vertices, faces = self.lines_to_faces(heights=heights, height_lines=height_lines)
        
        Store().storeRoom(vertices, faces) 
        
    def cluster_heights(self, minValue, maxValue, divider):
        jump = (maxValue - minValue) * divider
        numberOfJumps = int(np.ceil((maxValue - minValue) / jump))
        return [[minValue + jump * i, maxValue - jump * (numberOfJumps - i - 1)] for i in range(numberOfJumps)]
    
    def sort_clusters_for_height(self, clusters, heights):
        sorted_clusters = []
        for height in heights:
            print(height)
            height_clusters = []
            for cluster in clusters:
                height_cluster = []
                for vertex in cluster:
                    if vertex[2] >= height[0] and vertex[2] <= height[1]:
                        height_cluster.append(vertex)
                height_clusters.append(height_cluster)
            sorted_clusters.append(height_clusters)
        return sorted_clusters
    
    def lines_to_faces(self, heights, height_lines):
        vertices = []
        faces = []
        for i, lines in enumerate(height_lines):
            for line in lines:
                for i in range(1, len(line)):
                    x1, y1 = line[i-1]
                    x2, y2 = line[i]
                    face = []
                    face_vertices = [[x1, y1, heights[i][1]], [x2, y2, heights[i][1]], [x2, y2, heights[i][0]], [x1, y1, heights[i][0]]]
                    for v in face_vertices:
                        if v in vertices:
                            face.append(vertices.index(v)+1)
                        else:
                            face.append(len(vertices)+1)
                            vertices.append(v)
                    faces.append(face)
        return vertices, faces
                
                
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
            for i in range(len(cluster)):
                if cluster[i] == []:
                    continue
                val_x, val_y, _ = cluster[i]
                x.append(val_x)
                y.append(val_y)
                x1 = val_x if val_x < x1 else x1
                x2 = val_x if val_x > x2 else x2
                
            if (len(x) == 0 or len(y) == 0):
                continue
            x = np.array(x)
            y = np.array(y)
            a, b = np.polyfit(x,y,1)
            
            y1 = a*x1 + b
            y2 = a*x2 + b
            
            # plt.plot(x, y, 'o')
            # plt.plot(x, (a*x + b))
            lines.append([[x1, y1], [x2, y2]])
        # plt.show()
        return lines
    
    def connectLines(self, lines, distance_threshold): 
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
        connected_lines = [lines.pop(0)]
        has_reversed = False
        while len(lines) > 0: 
            point = connected_lines[-1][-1]
            best_distance = np.inf
            best = None
            idx = None 
            for i, line in enumerate(lines): 
                distance = [distPoints(point, x) for x in line]
                distance = [np.inf if x > distance_threshold else x for x in distance]
                if distance[0] < distance[1] and distance[0] < best_distance:
                    best_distance = distance[0]
                    best = line
                    idx = i
                elif distance[1] < best_distance:
                    best_distance = distance[1]
                    line.reverse()
                    best = line
                    idx = i
            if best is None: 
                if has_reversed:
                    connected_lines.append(lines.pop(0))
                    has_reversed = False
                else:
                    connected_lines[-1].reverse()
                    has_reversed = True
            else: 
                connected_lines[-1].extend(best)
                lines.pop(idx)
                has_reversed = False
        return connected_lines
            
    def rdp_angle(self, line, dist_threshold, angle_multiplier):   # Based on idea of rdp algorithm 
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
        
        length = len(line)
        while length >= 3:
            largestDiff = -np.inf
            idx = None
            for i in range(1, length):
                A = np.array(line[(i-1) % length])
                B = np.array(line[i])
                C = np.array(line[(i+1) % length])
                
                angle = points_angle(A, B, C)
                dist = point_line_distance(A, B, C)      
                dist = (dist * angle_multiplier) if angle >= 60 else dist
    
            
                if dist < dist_threshold: 
                    diff = dist_threshold - dist
                    if diff > largestDiff:
                        largestDiff = diff
                        idx = i
                        
            if idx is None: 
                return line
            else:
                line.pop(idx)
                length -= 1
        return line 