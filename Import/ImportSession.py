import requests
import json

from Log.Logging import Log

class ImportSession():

    @staticmethod
    def session_names() -> list:
        request = requests.get('http://130.240.202.87:3000/names')
        sessions = json.loads(request.text)['sessionNames']
        if (len(sessions) == 0):
            Log.error("No sessions available")
            exit()
        return [session['sessionName'] for session in sessions] 

    @staticmethod
    def session_points(session_name: str) -> list:
        request = requests.get('http://130.240.202.87:3000/' + session_name)
        points = json.loads(request.text)['points']
        points = [[y, x, z] for x, y, z in points]
        return points
    