import requests
import os
from dotenv import load_dotenv, set_key
load_dotenv('src/.env')
dot_env_path = "src/.env"

def execute_oauth2(header, payload):
    """
    This function allows the user to authenticate with his GitHub account.
    It is used to ask the oauth2 system to produce a device code in order to get the access token.

    :param header: the http header to make a request
    :param payload: the payload containing the secret client id
    :return: the device code needed to complete the authentication
    """ 

    r = requests.post('https://github.com/login/device/code',headers=header,json=payload)
    data = r.json()
    device_code = data['device_code']
    uri = data['verification_uri']
    user_code = data['user_code']
    print("[bold magenta]To authorize this app, go to {} and enter the code {}".format(uri,user_code))
    input('[bold magenta]Press any key to continue once you have input the code successfully')
    return device_code

def generate_new_token(header, payload):
    """
    This function is used to generate a new Personal Access Token through the GitHub API.
    It also stores the token in the environment.

    :param header: the http header to make a request
    :param payload: the payload containing the secret client id and the device code obtained with the authentication
    :return: the personal access token
    """ 
    r = requests.post( "https://github.com/login/oauth/access_token", headers=header, json=payload)
    set_key(dot_env_path, "PAT", r.json()['access_token'])   
    return r.json()['access_token']

def get_access_token():
    """
    This function is used to retrieve the personal access token either from the environment if stored or through a new GitHub authentication.

    :return: the personal access token
    """ 
    pat = os.environ.get('PAT',"")
    if not pat:
        print("[bold magenta]Retrieving Personal Access Token from GitHub")
        client_id = os.environ.get('CLIENT_ID',"")
        header = {"Content-Type": "application/json", "Accept": "application/json"}
        payload1 = {"client_id": client_id,}
        device_code = execute_oauth2(header, payload1)
        payload2 = {
            "client_id": client_id,
            "device_code": device_code,
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
        }
        pat = generate_new_token(header, payload2)
    else:
        print("[bold magenta]Retrieving stored Personal Access Token")
    return pat