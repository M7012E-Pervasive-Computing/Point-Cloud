import numpy as np

class SliceByHeight():
    
    @staticmethod
    def heights(point_cloud, divider):
        minValue = point_cloud.get_min_bound()[2]
        maxValue = point_cloud.get_max_bound()[2]
        jump = (maxValue - minValue) * divider
        numberOfJumps = int(np.ceil((maxValue - minValue) / jump))
        return [[minValue + jump * i, maxValue - jump * (numberOfJumps - i - 1)] for i in range(numberOfJumps)]
    
    @staticmethod
    def slice(point_clouds, heights):
        sorted_point_clouds = []
        for height in heights:
            height_point_clouds = []
            for point_cloud in point_clouds:
                height_point_cloud = []
                for vertex in point_cloud:
                    if vertex[2] >= height[0] and vertex[2] <= height[1]:
                        height_point_cloud.append(vertex)
                height_point_clouds.append(height_point_cloud)
            sorted_point_clouds.append(height_point_clouds)
        return sorted_point_clouds
    
    