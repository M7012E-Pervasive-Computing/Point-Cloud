
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
    def denoise(point_cloud: o3d.geometry.PointCloud) -> o3d.geometry.PointCloud:
        arguments = [
            {
                "ratio" : [0.05, 0.05],
                "neighbors" : [75, 25],
                "voxel_size" : 0.5,
            },
            {
                "ratio" : [0.05, 0.05],
                "neighbors" : [75, 25],
                "voxel_size" : 0.5,
            },
            {
                "ratio" : [0.05, 0.05],
                "neighbors" : [75, 25],
                "voxel_size" : 0.5,
            },
            {
                "ratio" : [0.05, 0.05],
                "neighbors" : [75, 25],
                "voxel_size" : 0.5,
            },
            {
                "ratio" : [0.05, 0.05],
                "neighbors" : [75, 25],
                "voxel_size" : 0.5,
            },
            {
                "ratio" : [0.05, 0.05],
                "neighbors" : [75, 25],
                "voxel_size" : 0.5,
            }
        ]
        denoised_clouds = []
        for i in range(len(arguments)):
            cloud = copy.deepcopy(point_cloud)
            cloud = Denoise.statistical_outlier(
                point_cloud=cloud, 
                ratio=arguments[i]["ratio"][0], 
                neighbors=arguments[i]["neighbors"][0])
            cloud = Downsampling.voxel_down(
                point_cloud=cloud,
                voxel_size=arguments[i]["voxel_size"])
            cloud = Denoise.statistical_outlier(
                point_cloud=cloud,
                ratio=arguments[i]["ratio"][1], 
                neighbors=arguments[i]["neighbors"][1])
            denoised_clouds.append(cloud)
        length = len(denoised_clouds)
        ProcessByInput._plot_point_clouds(
            point_clouds=denoised_clouds, 
            row=int(np.floor(length/2)),
            col=int(np.ceil(length/2)))
        Input.get_int_input(length, "Pick a cloud:\n")
    
    @staticmethod
    def _plot_point_clouds(point_clouds: list, row: int, col: int) -> None:
        figure = plt.figure(figsize=plt.figaspect(0.5))
        for r in range(row): 
            for c in range(col):
                ax = figure.add_subplot(row, col, (r, c), projection='3d')
                ax.set_title(f"{r*col+c}")
                point_cloud = point_clouds[r*col+c]
                points = np.asarray(point_cloud.points)
                x = [i for i, _, _ in points]
                y = [i for _, i, _ in points]
                z = [i for _, _, i in points]
                ax.plot(x, y, z)
        plt.show()
    
    
    
      
    