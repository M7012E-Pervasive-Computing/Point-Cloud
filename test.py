from open3d import geometry, utility, visualization
import numpy as np

#Create two random points
randomPoints = np.random.rand(2, 3)

pointSet = geometry.PointCloud()

pointSet.points = utility.Vector3dVector(randomPoints)

#Visualize the two random points
visualization.draw_geometries([pointSet])

#Here I want to add more points to the pointSet
#This solution does not work effective

#Create another random set
p1 = np.random.rand(3, 3)

p2 = np.concatenate((pointSet.points, p1), axis=0)

pointSet2 = geometry.PointCloud()

pointSet2.points = utility.Vector3dVector(p2)

visualization.draw_geometries([pointSet2])