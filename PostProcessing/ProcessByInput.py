
import open3d as o3d
import copy
import numpy as np
import matplotlib.pyplot as plt

from Helper.Input import Input

from PostProcessing.PointCloud.DenoiseOutlier import DenoiseOutlier as Denoise
from PostProcessing.PointCloud.Downsampling import Downsampling
from PostProcessing.PointCloud.Clustering import Clustering
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
        index = Input.get_int_input(length, "Pick a cloud:\n")
        return denoised_clouds[index]
        
    
    @staticmethod
    def _plot_point_clouds(point_clouds: list, row: int, col: int) -> None:
        color_map = plt.cm.get_cmap('RdYlBu')
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
                ax.scatter(x, y, z, c=z)
                ax.view_init(azim=0, elev=90)
        plt.show()
    
    
    
      
    