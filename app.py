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
    
    def patch(self, user_id):
        body = request.json
        user = synapse.update_user_status(user_id=user_id, body=body)
        return user

    @app.route('/bank/api/dev/users', methods=['POST'])
    def post(self):
        payload = request.json
        user = synapse.create_user(payload=payload)
        mongodb_client = MongoClient('localhost', 27107)
        db = mongodb_client['bank']

        entry = {
            'user_id': payload['_id'], 
            'document_id': payload['documents'][0]['id'],
            'legal_name' : payload['legal_names'][0],
            'refresh_token': payload['refresh_token']
        }
        # insert the entry into the database.
        post = db.posts
        post.insert_one(entry)
        return user

class Account(Resource):
    def get(self)


api.add_resource(User,'/bank/api/dev/users/<string:user_id>')

    

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

