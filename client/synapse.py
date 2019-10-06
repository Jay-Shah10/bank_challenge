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
        response = requests.get(url=user, headers=client_headers, verfiy=False)
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