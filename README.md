# Bank

## Summary
This is a backend challenge for synapse using their API as a platform to create a bank.
This was created using Flask framework to create API endpoints. The main bank app creates a user, view a user, update a user's info. It will also create a deposit account, view a user's account, and delete an account. 


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
This will run on you local machine. Click on the ```http://0.0.0.0:5000/bank/api/dev/users/user_id```.
This will show you the details on one user.



