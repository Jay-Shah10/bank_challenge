import json
from flask import Flask
from flask import jsonify
from flask import request
from flask_restful import Resource, Api
import pymongo
from pymongo import MongoClient
import configs
from client import synapse
from synapsepy import Client

CLIENT = Client(client_id=configs.CLIENT_ID,
                client_secret=configs.CLIENT_SECRET,
                fingerprint=configs.FINGERPRINT,
                ip_address=configs.IP_ADDRESS,
                devmode=True
)

app = Flask(__name__)
api = Api(app)



class User(Resource):
    def get(self, user_id):
        """ Get a specific user.""" 
        user = CLIENT.get_user(user_id=user_id)
        return user.body
    
    def patch(self, user_id):
        """
        Updating user information.
        """
        body = request.json
        user = CLIENT.get_user(user_id=user_id)
        updated = user.update_info(body=body)
        return updated
        
    @app.route('/bank/api/dev/users', methods=['POST'])
    def post(self):
        """
        This will create a user to synapse and also record in mongodb.
        """
        # creating user using synapsepy.
        payload = request.json()
        user = CLIENT.create_user(body=payload, ip=configs.IP_ADDRESS)

        # adding user to local database.
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
        return user.__dict__

class Account(Resource):
    def get(self, user_id):

        # n = synapse.Node()
        # node = n.get_user_node(user_id=user_id)
        user = CLIENT.get_user(user_id=user_id)
        nodes = user.get_all_nodes(page=4)
        return nodes
    
    def post(self, user_id):
        body = request.json()
        user = CLIENT.get_user(user_id)
        account = user.create_node(body=body)
        return account

    def patch(self, user_id):
        body = request.json()
        node_id = "5c8abccb4b7ba9102c674cdf"
        user = CLIENT.get_user(user_id)

        nodes = user.get_all_nodes(page=4)
        nodeid = nodes.__dict__['nodes'][0]['_id'] # node_id from response. Using example node id for this challenge.

        node = user.update_node(node_id, body)
        return node

    def delete(self, user_id, node_id):
        node_id = "5c8abccb4b7ba9102c674cdf"
        user = CLIENT.get_user(user_id)
        result = user.delete_node(node_id=node_id)
        return result

class DebitCard():
    def post(self, user_id, node_id):
        """Creating a debit card for a user."""
        pass

    
    
    



api.add_resource(User,'/bank/api/dev/users/<string:user_id>')
api.add_resource(Account, '/bank/api/dev/<string:user_id>/nodes/<string:node_id>')

    

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

