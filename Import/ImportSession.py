import requests
import json

class ImportSession():

    @staticmethod
    def names() -> list:
        request = requests.get('http://130.240.202.87:3000/names')
        sessions = json.loads(request.text)['sessionNames']
        if (len(sessions) == 0):
            print("No sessions available")
            exit()
        else:
            print("Successfully imported session names from database")
            return [session['sessionName'] for session in sessions] 

    @staticmethod
    def points(session_name: str) -> list:
        request = requests.get('http://130.240.202.87:3000/' + session_name)
        points = json.loads(request.text)['points']
        points = [[point['y'], point['x'], point['z']] for point in points]
        print(f"Successfully imported points from session: {session_name}")
        return points
    