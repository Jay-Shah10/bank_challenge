import json
from flask import Flask
from flask import jsonify
from flask import request
from flask_restful import Resource, Api
import pymongo
from pymongo import MongoClient
import configs
from client import synapse

app = Flask(__name__)
api = Api(app)


class User(Resource):
    def get(self, user_id):
        user = synapse.get_user(user_id=user_id)
        return user
    
    def post(self, user_id=None):
        user = synapse.create_user(payload=request.get_json())
        # update mongodb
        return user

api.add_resource(User,'/bank/api/dev/users/<string:user_id>')
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

