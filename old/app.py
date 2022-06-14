import requests
import json

from objects.PointCloud import PointCloud

from optimizing.DenoiseOutlier import DenoiseOutlier
from optimizing.Clustering import Clustering
from optimizing.Ransac import Ransac
from optimizing.Test import Test

from visualization.open3DPointCloud import Open3DPointCloud
# from visualization.pyvistaPointCloud import PyvistaPointCloud
from visualization.vizPointCloud import VisualizationPointCloud

import numpy as np

class App:
    """App for visualization of point clouds which are requested from point-service.
    """
    
    def __init__(self):
        # self.debug = False
        # if (input('Debug mode? (y/n)') == 'y'):
        #     self.debug = True
        self.session_name = self._request_session_names()
        points = self._request_session_points(self.session_name)
        points = np.array([
            [points[i]["y"],
            points[i]["x"],
            points[i]["z"]] 
            for i in range(len(points))])
    
        Test(points)
        
        # self.point_cloud = PointCloud(points, self.debug) 

        # if (input('Do you want to denoise the point cloud? (y/n)? ') == 'y'):
        #     self.should_denoise()
            
        # result = input('Do you want to cluster the points (y/n)? ')
        # if result == 'y':
        #     clustered_point_cloud = Clustering(self.point_cloud, True).cluster_data()    
        #     result = input('Do you want to apply Ransac (y/n)? ')
        #     if result == 'y':
        #         planeData = []
        #         for point_cloud in clustered_point_cloud:
        #             ransac = Ransac(point_cloud, self.debug)
        #             ransac.apply()
        #             planeData.extend(ransac.get_plane_data())
        #         self.write_obj_file(planeData)
        
        # self.visualization = self._select_visualization()
        # self.visualization.visualize()
        # if (input('Do you want to save the point cloud? (y/n)? ') == 'y'):
        #     self.save_point_cloud(self.point_cloud.point_cloud.points)

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
        # session_picked = self._get_int_input(len(sessions), sessions_str)
        session_picked = 25
        
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
        
        # visualization_picked = self._get_int_input(
        #     1, 'Pick visualization: \n[1] open3D \n[2] pyvista\n')
        
        # if (visualization_picked == 1):
        return Open3DPointCloud(self.point_cloud)
        # elif (visualization_picked == 2):
        #     return PyvistaPointCloud(self.point_cloud)
    
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
    
    def write_obj_file(self, planeData):
        print(planeData)
        planeData = self.remove_empty_arrays(planeData)
        print(planeData)
        f = open("test.obj", "w")
        for i in range(len(planeData)):
            for j in range(len(planeData[i])):
                f.write("v " + str(planeData[i][j][0]) + " " + str(planeData[i][j][1]) + " " + str(planeData[i][j][2]) + " 1.0" + "\n")
        print(len(planeData))
        for i in range(len(planeData)):
            # 1/1/1 2/2/1 4/3/1 3/4/1
            # f 1 2 3 4
            # f 8 7 6 5
            # f 4 3 7 8
            
            # f 5 1 4 8
            # f 5 6 2 1
            # f 2 6 7 3
            f.write("f " +
                    str(i * 8 + 1) + " " + str(i * 8 + 2) + " " + str(i * 8 + 3) + " " + str(i * 8 + 4) +"\n")
            f.write("f " +
                    str(i * 8 + 8) + " " + str(i * 8 + 7) + " " + str(i * 8 + 6) + " " + str(i * 8 + 5) +"\n")
            f.write("f " +
                    str(i * 8 + 4) + " " + str(i * 8 + 3) + " " + str(i * 8 + 7) + " " + str(i * 8 + 8) +"\n")
            
            f.write("f " +
                    str(i * 8 + 5) + " " + str(i * 8 + 1) + " " + str(i * 8 + 4) + " " + str(i * 8 + 8) +"\n")
            f.write("f " +
                    str(i * 8 + 5) + " " + str(i * 8 + 6) + " " + str(i * 8 + 2) + " " + str(i * 8 + 1) +"\n")
            f.write("f " +
                    str(i * 8 + 2) + " " + str(i * 8 + 6) + " " + str(i * 8 + 7) + " " + str(i * 8 + 3) +"\n")
            # f.write("f " +
            #         str(i * 4 + 1) + "/" + str(i * 4 + 1) + "/" + str(i * 4 + 1) + " " +
            #         str(i * 4 + 2) + "/" + str(i * 4 + 2) + "/" + str(i * 4 + 1) + " " +
            #         str(i * 4 + 4) + "/" + str(i * 4 + 3) + "/" + str(i * 4 + 1) + " " +
            #         str(i * 4 + 3) + "/" + str(i * 4 + 4) + "/" + str(i * 4 + 1) + "\n")
        f.close()

    def save_point_cloud(self, planeData):
        fileName = input("Enter file name: ")
        f = open(fileName + ".obj", "w")
        for i in range(len(planeData)):
            f.write("o " + fileName + "." + str(i) + "\n")
            f.write("v " + str(planeData[i][0]) + " " + str(planeData[i][1]) + " " + str(planeData[i][2]) + " 1.0" + "\n")
        f.close()
    
    def remove_empty_arrays(self, planeData):
        returnData = []
        for i in range(len(planeData)):
            if planeData[i] == []:
                continue
            returnData.append(planeData[i])
        return returnData

App()
    