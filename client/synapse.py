import json
import requests
import configs

client_headers = {
    'X-SP-USER-IP': configs.IP_ADDRESS,
    'X-SP-USER': f'|{configs.FINGERPRINT}',
    'X-SP-GATEWAY': f'{configs.CLIENT_ID}|{configs.CLIENT_SECRET}'
}

dev_url = 'https://uat-api.synapsefi.com/v3.1/'

def get_users():
    all_users = f'{dev_url}/users'
    try:
        response = requests.get(url=all_users,headers=client_headers,verify=False)
        return response.json()
    except Exception as exc:
        return exc

def get_user(user_id):
    user = f"{dev_url}/users/{user_id}"
    try: 
        response = requests.get(url=user, headers=client_headers, verify=False)
        return response.json()  
    except Exception as exc:
        return exc

def create_user(payload):
    create_user_url = f"{dev_url}/users"
    try:
        response = requests.post(url=create_user_url, headers=client_headers,verify=False)
        if response.status_code != 201:
            return response.json()
        else:
            return response.json()
    except Exception as exc:
        return exc

def update_user_status(user_id, body):
    user_url = f"{dev_url}/users/{user_id}"
    try:
        response = requests.patch(url=user_url,
                                 headers=client_headers, 
                                 data = body,
                                 verify=False)
        return response.json()
    except Exception as exc:
        return exc


def get_oauth(user_id, payload):
    res = get_user(user_id=id)
    res.json()['refresh_token']

    oauth = f"{dev_url}/oauth/{user_id}"
    try:
        response = requests.post(url=oauth, 
                                headers=client_headers,
                                data=payload, 
                                verify=False)
        return response.json()['oauth_key']
    except Exception as exc:
        return exc