from flask import Flask
from flask import jsonify
from flask_restful import Resource, Api
import configs
import json
from client import synapse

app = Flask(__name__)
api = Api(app)

# CLIENT = Client(client_id=configs.CLIENT_ID,
#                 client_secret=configs.CLIENT_SECRET,
#                 fingerprint=configs.FINGERPRINT,
#                 ip_address=configs.IP_ADDRESS,
#                 devmode=True
# )


@app.route('/bank/api/dev/users', methods=['GET', 'POST'])
def get_all_users():
    users = synapse.get_users()
    return users
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

