

import requests
import json
from optimizing.Optimizing import Optimizing

from visualization.open3DPointCloud import Open3DPointCloud
from visualization.pyvistaPointCloud import PyvistaPointCloud
from visualization.vizPointCloud import VisualizationPointCloud

class App:
    """App for visualization of point clouds which are requested from point-service.
    """
    
    def __init__(self):
        self.session_name = self._request_session_names()
        self.points = self._request_session_points(self.session_name)
        
        result = input('Optimize [y/n]')
        if result == 'y':
            self.points = Optimizing(self.points).optimize_data(ratio=0.2, neighbors=10)
            
        self.visualization = self._select_visualization()
        self.visualization.visualize()
            
    def _request_session_names(self) -> str:
        """Requests all session names from point-service and creates a string from the sessions.
        Then it request int input which is represented as a specific session name.
        Finally returning the chosen session str.  
        
        Returns:
            str: name of session
        """
        
        request = requests.get('http://130.240.202.87:3000/names')
        sessions = json.loads(request.text)
        
        sessions_str = 'Pick a session:\n'
        for i in range(len(sessions)):
            sessions_str += '[' + str(i + 1) + '] ' + str(sessions[i]) + '\n'
        session_picked = self._get_int_input(len(sessions), sessions_str)
        
        return sessions[session_picked - 1]
    
    def _request_session_points(self, session_name: str) -> list:
        """Request points from session which are requested from point-service.

        Args:
            session_name (str): name of session to be requested

        Returns:
            list: return a list of points
        """
        
        request = requests.get('http://130.240.202.87:3000/' + session_name)
        points = json.loads(request.text)
        return points
    
    def _select_visualization(self) -> VisualizationPointCloud:
        """Let user pick a visualization for point cloud.

        Returns:
            VisualizationPointCloud: return the visualization chosen 
        """
        
        visualization_picked = self._get_int_input(
            2, 'Pick visualization: \n[1] open3D \n[2] pyvista\n')
        
        if (visualization_picked == 1):
            return Open3DPointCloud(self.points)
        elif (visualization_picked == 2):
            return PyvistaPointCloud(self.points)
    
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
    