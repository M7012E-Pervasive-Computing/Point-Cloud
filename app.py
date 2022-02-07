from flask import Flask
from flask_restful import Api, Resource


app = Flask(__name__)
api = Api(app)
    
class pointData(Resource):
    pointList = [[]]
    def __init__(self, pointList):
        self.pointList = pointList
    
    def get(self):
        return {"points"}

api.add_resource(pointData, "/pointData")

if __name__ == "__app__":
    app.run(debug=True)

