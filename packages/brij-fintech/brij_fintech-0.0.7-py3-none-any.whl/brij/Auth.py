import requests
from requests.auth import HTTPBasicAuth
import os
from brij import urls

class Auth:
    
    def __init__(self, env='sandbox', app_id=None, app_key=None):
        self.env = env
        self.app_id = app_id
        self.app_key = app_key
        
        
    def authenticate(self):
        authenticate_url = '{}{}'.format(urls.base_url, urls.tokens)
        r = requests.get(authenticate_url,
                         auth=HTTPBasicAuth(self.app_id, self.app_key))

        assert ('token' in r.json()), 'check your credentials'
        self.token = r.json()['token']