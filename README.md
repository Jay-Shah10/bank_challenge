# Bank

## Summary
This is a backend challenge for synapse using their API as a platform to create a bank.
This was created using Flask framework to create API endpoints. The main bank app creates a user, view a user, update a user's info. It will also create a deposit account, view a user's account, and delete an account. 

## Requirements
```
Python3
MongoDB
synapsepy
pymongo
client id 
client secret
synapse sandbox account.
```

## How to
You will need python 3.
You will need to create a python virtual env. 
```
python3 -m venv venv
source venv/bin/activate
```

pip install from requirements.txt
```
pip -r install requirements.txt
```

* app.py contains the main functionality. Also contains endpoints.
* configs.py - contains creds/configurations.
* client/synapse.py  - contains synapse specfic APIs.

Activate the Python Virtual env and run app.py
```
source venv/bin/activate
python app.py
```
This will run on you local machine. Click on the ```http://0.0.0.0:5000```.

To view user: 
append: ```/bank/api/dev/users/<user_id>``` this user_id is a test id used for this challenge's purpose.

To view Transactions/nodes.
append: ```/bank/api/dev/users/<user_id>/nodes/<node_id>/transaction/None```.
None is added since get() does not need a node_id.
results should be: 
```
{
    "page": 1,
    "page_count": 0,
    "limit": 20,
    "trans_count": 0,
    "list_of_trans": []
}
```

To view Card: 
append: ```/bank/api/dev/users/user_id/nodes/node_id/card```
result: should be an error. did not create an example card.
```
synapsepy.errors.ObjectNotFound: Unable to locate subnet object with ID <user_id> for node <node_id> of user <user_id>
```

Results directory contains results found on screen.


## Resources
* [Synapse API](https://docs.synapsefi.com/reference#api-initialization)
* [Synapse getting started](https://docs.synapsefi.com/docs/getting-started)
* [Flask API](https://flask-restful.readthedocs.io/en/latest/quickstart.html#)
* [pymongo](https://api.mongodb.com/python/current/tutorial.html)
 


## Author
* Jay Shah

