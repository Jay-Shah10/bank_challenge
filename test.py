import configs
# from synapsepy import Client, User
import json
import requests
# CLIENT = Client(client_id=configs.CLIENT_ID,
#                 client_secret=configs.CLIENT_SECRET,
#                 fingerprint=configs.FINGERPRINT,
#                 ip_address=configs.IP_ADDRESS,
#                 devmode=True
# )

client_headers = {
    'X-SP-USER-IP': configs.IP_ADDRESS,
    'X-SP-USER': f'|{configs.FINGERPRINT}',
    'X-SP-GATEWAY': f'{configs.CLIENT_ID}|{configs.CLIENT_SECRET}'
}
dev_url = 'https://uat-api.synapsefi.com/v3.1/'


def get_users():
    all_users = f'{dev_url}/users/5d98116892571b46e3501246'
    response = requests.get(url=all_users,headers=client_headers,verify=False)
    print(json.dumps(response.json(), indent=2))


    
def create_account():
    user_headers = {
            'X-SP-USER-IP':configs.IP_ADDRESS ,
            'X-SP-USER': f'{configs.OAUTH_TOKEN}|{configs.FINGERPRINT}'
        }
    url = f'{dev_url}users/5d98116892571b46e3501246/nodes'
    payload = {
            "type":"Deposit-US",
            "info": {
                "nickname": "My deposit Account"
            }
        }
    try: 
        response = requests.post(url=url,
                                    headers=user_headers, 
                                    data=payload, 
                                    verify=False)
        return response.json()
    except Exception as exc:
            return exc
    


if __name__ == "__main__":
    create_account()