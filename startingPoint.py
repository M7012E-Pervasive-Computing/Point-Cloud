import numpy as np

import pyvista as pv
from pyvista import examples

# Define some helpers - ignore these and use your own data!
def generate_points(subset=0.02):
    """A helper to make a 3D NumPy array of points (n_points by 3)"""
    dataset = examples.download_lidar()
    ids = np.random.randint(low=0, high=dataset.n_points-1,
                            size=int(dataset.n_points * subset))
    return dataset.points[ids]


points = generate_points()
# Print first 5 rows to prove its a numpy array (n_points by 3)
# Columns are (X Y Z)
points[0:5, :]

print(len(points))

point_cloud = pv.PolyData(points)
np.allclose(points, point_cloud.points)

# Make data array using z-component of points array
data = points[:,-1]

# Add that data to the mesh with the name "uniform dist"
point_cloud["elevation"] = data

point_cloud.plot(render_points_as_spheres=True)
