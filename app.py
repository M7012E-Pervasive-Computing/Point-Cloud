import requests
import json

import os

from objects.PointCloud import PointCloud

from optimizing.DenoiseOutlier import DenoiseOutlier
from optimizing.Clustering import Clustering
from optimizing.Ransac import Ransac

from visualization.open3DPointCloud import Open3DPointCloud
from visualization.pyvistaPointCloud import PyvistaPointCloud
from visualization.vizPointCloud import VisualizationPointCloud

import numpy as np

class App:
    """App for visualization of point clouds which are requested from point-service.
    """
    
    def __init__(self):
        self.debug = False
        if (input('Debug mode? (y/n)') == 'y'):
            self.debug = True
        self.session_name = self._request_session_names()
        points = self._request_session_points(self.session_name)
        points = np.array([
            [points[i]["x"],
            points[i]["y"],
            points[i]["z"]] 
            for i in range(len(points))])
        
        self.point_cloud = PointCloud(points, self.debug) 

        if (input('Do you want to denoise the point cloud? (y/n)? ') == 'y'):
            self.should_denoise()
            
        result = input('Do you want to cluster the points (y/n)? ')
        if result == 'y':
            clustered_point_cloud = Clustering(self.point_cloud, self.debug).cluster_data()    
            # result = input('Do you want to apply Ransac (y/n)? ')
            # if result == 'y':
            #     planeData = []
            #     for point_cloud in clustered_point_cloud:
            #         ransac = Ransac(point_cloud, self.debug)
            #         ransac.apply()
            #         planeData.extend(ransac.get_plane_data())
            #     print(planeData)
            import pyvista as pv
            color = np.array(['red', 'blue', 'green', 'yellow', 'orange', 'pink'])
            p = pv.Plotter(shape=(1, 1))
            for c in clustered_point_cloud: 
                col = np.random.choice(color)
                
                cloud = c.get()
                center = cloud.get_center()
                max = cloud.get_max_bound()
                min = cloud.get_min_bound()
                print(f"max: {max} \tmin: {min}")
                # cube = pv.Cube(
                #     center=center, 
                #     x_length=np.abs(max[0]) + np.abs(min[0]), 
                #     y_length=np.abs(max[1]) + np.abs(min[1]), 
                #     z_length=np.abs(max[2]) + np.abs(min[2]))
                cube = pv.Cube(center=center, bounds=(min[0], max[0], min[1], max[1], min[2], max[2]))
                
                # p2 = pv.Plotter(shape=(1,2))
                # p2.add_mesh(c.get_pv(), color=col, show_edges=True)
                # p2.subplot(0, 1)
                # p2.add_mesh(cube, color=col, show_edges=True)
                # p2.show()
                
                # p.subplot(0,0)
                p.add_mesh(c.get_pv(), color=col, show_edges=True)
                # p.subplot(0,1)
                p.add_mesh(cube, color=col, show_edges=True, opacity=0.5)
            p.show()
               
                
                
        
        self.visualization = self._select_visualization()
        self.visualization.visualize()

    def should_denoise(self):
        """Denoise point cloud with either Statistical outlier or Radius outlier recursively 
        """
        denoise = DenoiseOutlier(self.point_cloud, self.debug)
        while (True):
            result = input('Denoise point cloud with: \n[1] Statistical outlier \n[2] Radius outlier \n[3] Exit\n')
            if result == '1':
                denoise.statistical_outlier(ratio=0.2, neighbors=10)
            elif result == '2':
                denoise.radius_outlier(nb_points=12, radius=0.10)
            elif result == '3' or result == 'exit':
                self.point_cloud = denoise.get_point_cloud()
                break

    def _request_session_names(self) -> str:
        """Requests all session names from point-service and creates a string from the sessions.
        Then it request int input which is represented as a specific session name.
        Finally returning the chosen session str.  
        
        Returns:
            str: name of session
        """
        
        request = requests.get('http://130.240.202.87:3000/names')
        # sessions = json.loads(request.text) # Old service
        sessions = json.loads(request.text)['sessionNames'] # new service
        if (len(sessions) == 0):
            print('No sessions available')
            exit()
        sessions_str = 'Pick a session:\n'
        for i in range(len(sessions)):
            # sessions_str += '[' + str(i + 1) + '] ' + str(sessions[i]) + '\n' # Old service
            sessions_str += '[' + str(i + 1) + '] ' + str(sessions[i]['sessionName']) + '\n' # New service
        session_picked = self._get_int_input(len(sessions), sessions_str)
        
        # return sessions[session_picked - 1] # Old service
        return sessions[session_picked - 1]['sessionName'] # new service
    
    def _request_session_points(self, session_name: str) -> list:
        """Request points from session which are requested from point-service.

        Args:
            session_name (str): name of session to be requested

        Returns:
            list: return a list of points
        """
        
        request = requests.get('http://130.240.202.87:3000/' + session_name)
        # points = json.loads(request.text) # Old service
        points = json.loads(request.text)['points'] # New service
        return points
    
    def _select_visualization(self) -> VisualizationPointCloud:
        """Let user pick a visualization for point cloud.

        Returns:
            VisualizationPointCloud: return the visualization chosen 
        """
        
        visualization_picked = self._get_int_input(
            2, 'Pick visualization: \n[1] open3D \n[2] pyvista\n')
        
        if (visualization_picked == 1):
            return Open3DPointCloud(self.point_cloud)
        elif (visualization_picked == 2):
            return PyvistaPointCloud(self.point_cloud)
    
    def _get_int_input(self, max: int, print_str: str = ''): 
        """Help function which returns a valid int between 1 and max, which is given by user. 

        Args:
            max (int): valid maximum of input int 
            print_str (str, optional): str to be printed on input. Defaults to ''.

        Returns:
            _type_: _description_
        """
        
        result = 0
        while True:
            try:
                result = int(input(print_str))
                if result > max or result < 1: 
                    print('Not a valid index')
                    continue
                break
            except ValueError:
                print('Not a valid input')
        return result
    
App()
    