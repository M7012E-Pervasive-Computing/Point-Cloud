
from ast import arguments
import open3d as o3d
import copy
import numpy as np
import matplotlib.pyplot as plt

from Helper.Input import Input

from PostProcessing.PointCloud.DenoiseOutlier import DenoiseOutlier as Denoise
from PostProcessing.PointCloud.Downsampling import Downsampling
from PostProcessing.PointCloud.Cluster import Cluster
from PostProcessing.PointCloud.SliceByHeight import SliceByHeight
from PostProcessing.PointCloud.CreateLines import CreateLines

from PostProcessing.Line.ConnectLines import ConnectLines
from PostProcessing.Line.RamerDouglasPeucker import RamerDouglasPeucker
from PostProcessing.Line.CreateFaces import CreateFaces

class ProcessByInput():
    
    @staticmethod
    def _createPointCloud(points: list, debug=False) -> o3d.geometry.PointCloud:
        point_cloud = o3d.geometry.PointCloud()
        point_cloud.points = o3d.utility.Vector3dVector(points)
        point_cloud.paint_uniform_color([0, 0, 0])
        if debug:
            o3d.visualization.draw_geometries([point_cloud])  
        return point_cloud  
    
    @staticmethod
    def _denoise(point_cloud: o3d.geometry.PointCloud) -> o3d.geometry.PointCloud:
        arguments = [
            {"ratio" : [0.05, 0.05],    "neighbors" : [150, 50],    "voxel_size" : 0.5},
            {"ratio" : [0.05, 0.05],    "neighbors" : [75, 25],     "voxel_size" : 0.5},
            {"ratio" : [0.05, 0.05],    "neighbors" : [50, 20],     "voxel_size" : 0.5},
            {"ratio" : [0.05, 0.05],    "neighbors" : [40, 15],     "voxel_size" : 0.5},
            {"ratio" : [0.05, 0.05],    "neighbors" : [100, 50],    "voxel_size" : 0.2},
            {"ratio" : [0.05, 0.05],    "neighbors" : [100, 50],    "voxel_size" : 0.1}
        ]
        denoised_clouds = []
        for arg in arguments:
            cloud = copy.deepcopy(point_cloud)
            cloud = Denoise.statistical_outlier(
                point_cloud=cloud, 
                ratio=arg["ratio"][0],
                neighbors=arg["neighbors"][0])
            cloud = Downsampling.voxel_down(
                point_cloud=cloud,
                voxel_size=arg["voxel_size"])
            cloud = Denoise.statistical_outlier(
                point_cloud=cloud,
                ratio=arg["ratio"][1],
                neighbors=arg["neighbors"][1])
            denoised_clouds.append(cloud)
        length = len(denoised_clouds)
        ProcessByInput._plot_point_clouds(
            point_clouds=denoised_clouds, 
            row=2,
            col=int(np.ceil(length/2)))
        index = Input.get_int_input(max=length, print_str="Pick a cloud:\n")
        return denoised_clouds[index]
    
    @staticmethod
    def _cluster(point_cloud: o3d.geometry.PointCloud) -> list:
        arguments = [
            {"eps" : 1,     "min_points" : 75},
            {"eps" : 0.8,   "min_points" : 75},
            {"eps" : 0.7,   "min_points" : 75},
            {"eps" : 0.6,   "min_points" : 75},
            {"eps" : 0.4,   "min_points" : 75},
            {"eps" : 0.2,   "min_points" : 75}
        ]
        clustered_points = []
        for arg in arguments:
            cloud = copy.deepcopy(point_cloud)
            cluster = Cluster.clustering(
                point_cloud=cloud,
                eps=arg["eps"], 
                min_points=arg["min_points"])
            clustered_points.append(cluster)
        length = len(clustered_points)
        
        point_clouds = []
        colors = []
        for clusters in clustered_points:
            points = []
            color = []
            for i, cluster in enumerate(clusters):
                points.extend(cluster)
                color.extend([i for _ in range(len(cluster))])
            point_clouds.append(ProcessByInput._createPointCloud(points=points))
            colors.append(color)
        ProcessByInput._plot_point_clouds(
            point_clouds=point_clouds, 
            row=2,
            col=int(np.ceil(length/2)), 
            colors=colors)
        index = Input.get_int_input(max=length, print_str="Pick a cloud:\n")
        return clustered_points[index]
    
    @staticmethod
    def _height(minValue: float, maxValue: float, point_clouds_points: list) -> tuple:
        option = Input.get_int_input(
            max=3, 
            print_str="Select height option:\n[0] No height\n[1] Height division\n[2] Uniform max height\n")
        heights = [[minValue, maxValue]]
        if option == 1 or option == 2:
            heights = SliceByHeight.heights(minValue=minValue, maxValue=maxValue, divider=0.1)
            heights = [[minValue, maxValue] for _ in heights] if option == 2 else heights
            
        height_slices = SliceByHeight.slice(point_clouds_points=point_clouds_points, heights=heights)
        return heights, height_slices
    
    @staticmethod
    def _point_cloud_to_lines(heights: list, height_slices: list):
        
        arguments = [
            {"distance_threshold" : [3, 2.25],  "angle_multiplier" : 1.25},
            {"distance_threshold" : [3, 0],     "angle_multiplier" : 1.25},
            {"distance_threshold" : [2, 1.5],   "angle_multiplier" : 1.25},
            {"distance_threshold" : [2, 0],     "angle_multiplier" : 1.25},
            {"distance_threshold" : [1, 0.75],  "angle_multiplier" : 1.25},
            {"distance_threshold" : [1, 0],     "angle_multiplier" : 1.25}]
        
        lines_options = []
        for args in arguments:
            height_lines = []
            for slice in height_slices:
                lines = CreateLines.point_clouds_to_lines(point_clouds=slice)
                lines = ConnectLines.connect(
                    lines=lines, 
                    distance_threshold=args["distance_threshold"][0])
                simplified_lines = []
                for line in lines:
                    simplified_line = RamerDouglasPeucker.rdp_angle(
                        line=line, 
                        distance_threshold=args["distance_threshold"][1], 
                        angle_multiplier=args["angle_multiplier"])
                    simplified_lines.append(simplified_line)
                height_lines.append(simplified_lines)
            lines_options.append(height_lines)
        
        length = len(lines_options)
        ProcessByInput._plot_lines(
            lines_options=lines_options, 
            heights=heights,
            row=2,
            col=int(np.ceil(length/2)))
        index = Input.get_int_input(max=length, print_str="Pick a line cloud:\n")
        return lines_options[index]
        
    @staticmethod
    def _plot_point_clouds(point_clouds: list, row: int, col: int, colors=None) -> None:
        figure = plt.figure(figsize=plt.figaspect(0.5))
        for r in range(row): 
            for c in range(col):
                index = r*col+c
                ax = figure.add_subplot(row, col, index+1, projection='3d')
                ax.set_title(f"{index}")
                point_cloud = point_clouds[index]
                points = np.asarray(point_cloud.points)
                x = [i for i, _, _ in points]
                y = [i for _, i, _ in points]
                z = [i for _, _, i in points]
                ax.scatter(x, y, z, c=(z if colors is None else colors[index]))
                ax.view_init(azim=0, elev=90)
        plt.show()
        
    @staticmethod
    def _plot_lines(lines_options: list, heights: list, row: int, col: int) -> None:
        figure = plt.figure(figsize=plt.figaspect(0.5))
        for r in range(row): 
            for c in range(col):
                index = r*col+c
                ax = figure.add_subplot(row, col, index+1, projection='3d')
                line_option = lines_options[index] 
                for i, lines_per_height in enumerate(line_option):
                    for line in lines_per_height:
                        x = [i for i, _ in line]
                        y = [i for _, i in line]
                        z = [heights[i][0] for _ in x]
                        ax.plot(x, y, z)
                ax.view_init(azim=0, elev=90)
        plt.show()
    
    
      
    