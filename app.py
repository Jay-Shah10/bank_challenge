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
        user_collection = db['user_collection']
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
        """
        body = {
            "type": "DEPOSIT-US",
            "info": {
                "nickname": "My Deposit Account",
                "document_id": "2a4a5957a3a62aaac1a0dd0edcae96ea2cdee688ec6337b20745eed8869e3ac8"
                }
            }
        """
        payload = request.json()
        user = CLIENT.get_user(user_id)
        account = user.create_node(body=payload)

        # Adding transaction to local mongodb.
        mongodb_client = MongoClient('localhost', 27107)
        db = mongodb_client['bank']
        account_collection = db['account_collection']
        entry = {
            'transaction_type': payload['type'],
            'information': payload['info']['nickname']
        }
        post = db.posts
        post.insert_one(entry)

        return account

    def patch(self, user_id):
        body = request.json()
        node_id = "5c8abccb4b7ba9102c674cdf"
        user = CLIENT.get_user(user_id)

        # nodes = user.get_all_nodes(page=4)
        # nodeid = nodes.__dict__['list_of_nodes'][0]['_id'] # node_id from response. Using example node id for this challenge.

        node = user.update_node(node_id, body)
        # add mongodb query to update.
        return node

    def delete(self, user_id, node_id):
        node_id = "5c8abccb4b7ba9102c674cdf"
        user = CLIENT.get_user(user_id)
        result = user.delete_node(node_id=node_id)
        # add mongodb query to delete.
        return result

class DebitCard():

    def post(self, user_id, node_id):
        """Creating a debit card for a user.
        body = {
                "nickname":"My Debit Card",
                "account_class":"DEBIT_CARD"
            }
        
        """
        user = CLIENT.get_user(user_id=user_id)

        # nodes = user.get_all_nodes(page=4)
        # nodeid = nodes.__dict__['list_of_nodes'][0]['_id'] # debut shows that nodes has key "list_of_nodes" instead of "nodes" as doc

        node_id = "5c8abccb4b7ba9102c674cdf" # using this as a test.
        payload = request.json
        debitcard = user.create_subnet(node_id=node_id, body=payload)

        mongodb_client = MongoClient('localhost', 27107)
        db = mongodb_client['bank']
        db['card_collection']
        entry = {
            'name': payload['nickname'],
            'account': payload['account_class']
        }
        post = db.posts
        post.insert_one(entry)

        return debitcard.__dict__
    
    def get(self, user_id, node_id):
        subnet_id="59c9f77cd412960028b99d2b" # using example for the challenge.
        user = CLIENT.get_user(user_id=user_id)
        debitcard = user.get_subnet(node_id, subnet_id=subnet_id)
        return debitcard.__dict__
    
    def patch(self, user_id, node_id):
        """
        Updating user's debit card.
        body example: 
        body = {
                "status": "ACTIVE",
                "card_pin": "1234",
                "preferences": {
                "allow_foreign_transactions": True,
                "daily_atm_withdrawal_limit": 10,
                "daily_transaction_limit": 1000
                }
            }
        returns: updated card information.
        To Delete card: 
        send this as body: 
        body = {
            "status":"TERMINATED"
            }
        """
        subnet_id="59c9f77cd412960028b99d2b" # using example for the challenge.
        body = request.json
        user = CLIENT.get_user(user_id=user_id)
        updatedcard = user.update_subnet(node_id=node_id, subnet_id=subnet_id, body=body)
        # add mongodb query to update.
        return updatedcard.__dict__

class Transaction():

    @app.route('/bank/api/dev/users/<string:user_id>/transaction', methods=['GET'])
    def get(self, user_id):
        """shows all transaction for a user."""
        user = CLIENT.get_user(user_id=user_id)
        trans = user.get_all_trans()
        return trans.__dict__

    def post(self, user_id, node_id):
        """
        creating a transaction for a user.
        body for the payload: 

        body = {
                "to": {
                    "type": "DEPOSIT-US",
                    "id": "5c8ac55542edab2b2665cbf1"
                },
                "amount": {
                    "amount": 100.1,
                    "currency": "USD"
                },
                "extra": {
                    "ip": "127.0.0.1",
                    "note": "Test transaction"
                }
            }
        """
        payload = request.json # body
        node_id = "5c8abccb4b7ba9102a61010d"
        user = CLIENT.get_user(user_id=user_id)

        # nodes = user.get_all_nodes(page=4)
        # nodeid = nodes.__dict__['list_of_nodes'][0]['_id']

        trans = user.create_trans(node_id, body=payload)

        mongodb_client = MongoClient('localhost', 27107)
        db = mongodb_client['bank']
        db['transactions_collection']
        entry = {
            "to": {
                    "type": payload['to']['type'],
                    "id": payload['to']['id']
                },
                "amount": {
                    "amount": payload['amount']['amount'],
                    "currency": payload['amount']['currency']
                },
                "extra": {
                    "note": payload['extra']['note']
                }
        }
        post = db.posts
        post.insert_one(entry)

        
        return trans.__dict__

        def patch(self, user_id, node_id):
            """
            Comment on a transcation.
            send in comment in json.
            {
                "comment": "your comment"
            }
            """
            comment = request.json()['comment']
            user = CLIENT.get_user(user_id=user_id)

            # trans = user.get_all_trans(page=4)
            # transid = trans.__dict__['list_of_trans'][0]['_id'] # grabbing the first id. need to iterate for more.

            trans_id = '5c78268a279caa0067e486e2' # using this for example.
            node_id = "5c8abccb4b7ba9102a61010d" # using this as an example.
            comment = user.comment_trans(node_id=node_id, trans_id=trans_id, comment=comment)
            return comment

        @app.route('/bank/api/dev/users/<string:user_id>/nodes/<string:node_id>/trans/<string:trans_id>', methods=["DELETE"])
        def delete(self, user_id, node_id, trans_id):
            """
            Cancel a transaction.
            """
            # using these as examples.
            nodeid = "5c8abccb4b7ba9102a61010d"
            transid = '5c8aced0af7f7525a298d64b'

            user = CLIENT.get_user(user_id=user_id)
            cancel = user.cancel_trans(node_id=nodeid, trans_id=transid)
            return cancel



api.add_resource(User,'/bank/api/dev/users/<string:user_id>')
api.add_resource(Account, '/bank/api/dev/users/<string:user_id>/nodes/<string:node_id>')
api.add_resource(DebitCard, 'bank/api/dev/users/<string:user_id>/nodes/<string:node_id>')
api.add_resource(Transaction, '/bank/api/dev/users/<string:user_id>/nodes/<string:node_id>')

    

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

