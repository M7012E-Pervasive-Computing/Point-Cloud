import open3d as o3d
import copy
import numpy as np
import matplotlib.pyplot as plt

from Helper.Input import Input
from Helper.CreatePointCloud import CreatePointCloud

from PostProcessing.PointCloud.DenoiseOutlier import DenoiseOutlier as Denoise
from PostProcessing.PointCloud.Downsampling import Downsampling
from PostProcessing.PointCloud.Cluster import Cluster
from PostProcessing.PointCloud.SliceByHeight import SliceByHeight
from PostProcessing.PointCloud.CreateLines import CreateLines

from PostProcessing.Line.ConnectLines import ConnectLines
from PostProcessing.Line.RamerDouglasPeucker import RamerDouglasPeucker
from PostProcessing.Line.CreateFaces import CreateFaces

class ProcessBySetting():
    
    @staticmethod
    def apply_post_setting_processing(points: list) -> tuple:
        """Apply all setting based post processing.

        Args:
            points (list): list of points as [x, y, z].

        Returns:
            tuple: all vertices as [x, y, z] and faces as list of vertex indices.
        """
        point_cloud = CreatePointCloud.open3d(points=points)
        point_cloud = ProcessBySetting.__denoise(point_cloud=point_cloud)
        clustered_points = ProcessBySetting.__cluster(point_cloud=point_cloud)
        min = point_cloud.get_min_bound()[2]
        max = point_cloud.get_max_bound()[2]
        uniform, heights, height_slices = ProcessBySetting.__height(
            minValue=min, maxValue=max, point_clouds_points=clustered_points)
        lines = ProcessBySetting.__point_cloud_to_lines(heights=heights, height_slices=height_slices)
        return CreateFaces.lines_to_faces([[min, max] for _ in heights] if uniform else heights, lines)

    @staticmethod
    def __denoise(point_cloud: o3d.geometry.PointCloud) -> o3d.geometry.PointCloud:
        """Denoise a open3d point cloud.

        Args:
            point_cloud (o3d.geometry.PointCloud): Point cloud to denoise.

        Returns:
            o3d.geometry.PointCloud: Resulting point cloud.
        """
        while True:
            try:
                ratio = float(input("Denoise ratio?:\n> "))
                neighbors = int(input("Denoise neighbors?:\n> "))
                cloud = copy.deepcopy(point_cloud)
                cloud = Denoise.statistical_outlier(
                    point_cloud=point_cloud,
                    ratio=ratio,
                    neighbors=neighbors
                )
                ProcessBySetting.__plot_point_cloud(cloud)
                if (input("Redo denoise (y/n)?:\n> ") != "y"):
                    point_cloud = cloud
                    break
            except KeyboardInterrupt:
                exit()
            except:
                print("Bad input")
                continue
        
        while True:
            try:
                voxel_size = float(input("Voxel size?:\n> "))
                cloud = copy.deepcopy(point_cloud)
                cloud = Downsampling.voxel_down(
                    point_cloud=point_cloud,
                    voxel_size=voxel_size
                )
                ProcessBySetting.__plot_point_cloud(cloud)
                if (input("Redo voxel down (y/n)?:\n> ") != "y"):
                    point_cloud = cloud
                    break
            except KeyboardInterrupt:
                exit()
            except:
                print("Bad input")
                continue
        
        while True:
            try:
                ratio = float(input("Denoise ratio?:\n> "))
                neighbors = int(input("Denoise neighbors?:\n> "))
                cloud = copy.deepcopy(point_cloud)
                cloud = Denoise.statistical_outlier(
                    point_cloud=point_cloud,
                    ratio=ratio,
                    neighbors=neighbors
                )
                ProcessBySetting.__plot_point_cloud(cloud)
                if (input("Redo denoise (y/n)?:\n> ") != "y"):
                    return cloud
            except KeyboardInterrupt:
                exit()
            except:
                print("Bad input")
                continue

    @staticmethod
    def __cluster(point_cloud: o3d.geometry.PointCloud) -> list:
        """Cluster open3d point cloud.

        Args:
            point_cloud (o3d.geometry.PointCloud): Point cloud to cluster.

        Returns:
            list: All clusters as list of [x, y, z].
        """
        
        while True:
            try:
                eps = float(input("Cluster eps?:\n> "))
                min_points = int(input("Cluster min_points?:\n> "))
                cloud = copy.deepcopy(point_cloud)
                clusters = Cluster.clustering(
                    point_cloud=cloud,
                    eps=eps,
                    min_points=min_points)
                points = []
                colors = []
                for i, cluster in enumerate(clusters):
                    points.extend(cluster)
                    colors.extend([i for _ in range(len(cluster))])
                cloud = CreatePointCloud.open3d(points=points)
                ProcessBySetting.__plot_point_cloud(
                    point_cloud=cloud, 
                    colors=colors)
                if (input("Redo clustering (y/n)?:\n> ") != "y"):
                    return clusters
            except KeyboardInterrupt:
                exit()
            except:
                print("Bad input")
                continue

    @staticmethod
    def __height(minValue: float, maxValue: float, point_clouds_points: list) -> tuple:
        """Slice a list of list containing points.

        Args:
            minValue (float): Min height (z axis).
            maxValue (float): Max height (z axis).
            point_clouds_points (list): List of list containing points as [x, y, z].

        Returns:
            tuple: heights and sliced points by height.
        """
        option = Input.get_int_input(
            max=3,
            print_str="Pick height option:\n[0] No height\n[1] Height division\n[2] Uniform max height\n> ")
        heights = [[minValue, maxValue]]
        uniform = option == 2
        if option == 1 or option == 2:
            heights = SliceByHeight.heights(
                minValue=minValue, maxValue=maxValue, divider=0.1)

        height_slices = SliceByHeight.slice(
            point_clouds_points=point_clouds_points, heights=heights)
        return uniform, heights, height_slices

    @staticmethod
    def __point_cloud_to_lines(heights: list, height_slices: list) -> tuple:
        """Turn a sliced list of points into lines.

        Args:
            heights (list): Heights levels for points.
            height_slices (list): sliced clusters of points by heights.

        Returns:
            tuple: all vertices as [x, y, z] and faces as list of vertex indices.
        """
        while True:
            try:
                distance_threshold = float(input("Point to line distance threshold?:\n> "))
                simplification_threshold = float(input("Line simplification distance threshold?:\n> "))
                angle_multiplier = float(input("Line simplification angle multiplier?:\n> "))
                
                height_lines = []
                for slice in height_slices:
                    lines = CreateLines.point_clouds_to_lines(point_clouds=slice)
                    lines = ConnectLines.connect(
                        lines=lines,
                        distance_threshold=distance_threshold)
                    simplified_lines = []
                    for line in lines:
                        simplified_line = RamerDouglasPeucker.rdp_angle(
                            line=line,
                            distance_threshold=simplification_threshold,
                            angle_multiplier=angle_multiplier)
                        simplified_lines.append(simplified_line)
                    height_lines.append(simplified_lines)

                ProcessBySetting.__plot_lines(
                    lines=height_lines,
                    heights=heights)

                if (input("Redo lines (y/n)?:\n> ") != "y"):
                    return height_lines
            except KeyboardInterrupt:
                exit()
            except:
                print("Bad input")
                continue

    @staticmethod
    def __plot_point_cloud(point_cloud: o3d.geometry.PointCloud, colors=None) -> None:
        """Plot a point cloud.

        Args:
            point_cloud (o3d.geometry.PointCloud): Point cloud.
            colors (list, optional): Color setting of each plot. Defaults to None.
        """
        figure = plt.figure(figsize=plt.figaspect(0.5))
        ax = figure.add_subplot(1, 1, 1, projection='3d')
        points = np.asarray(point_cloud.points)
        x = [i for i, _, _ in points]
        y = [i for _, i, _ in points]
        z = [i for _, _, i in points]
        ax.scatter(x, y, z, c=(z if colors is None else colors))
        ax.view_init(azim=0, elev=90)
        plt.show()

    @staticmethod
    def __plot_lines(lines: list, heights: list) -> None:
        """Plot a list of lines.

        Args:
            lines (list): List of lines.
            heights (list): Heights for all lines.
        """
        figure = plt.figure(figsize=plt.figaspect(0.5))
        ax = figure.add_subplot(1, 1, 1, projection='3d')
        for i, lines_per_height in enumerate(lines):
            for line in lines_per_height:
                x = [i for i, _ in line]
                y = [i for _, i in line]
                z = [heights[i][0] for _ in x]
                ax.plot(x, y, z)
        ax.view_init(azim=0, elev=90)
        plt.show()
