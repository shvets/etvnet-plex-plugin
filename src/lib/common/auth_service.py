import json
import time

try:
    from urlparse import urljoin
except:
    from urllib.parse import urljoin

from http_service import HttpService

class AuthService(HttpService):
    def __init__(self, auth_url, client_id, client_secret, grant_type, scope):
        self.auth_url = auth_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.grant_type = grant_type
        self.scope = scope

    def get_activation_codes(self, include_client_secret=True):
        data = {'scope': self.scope}

        if include_client_secret:
            data['client_secret'] = self.client_secret

        response = self.auth_request(data, 'device/code')

        result = json.loads(response)

        result['activation_url'] = self.auth_url + 'device/usercode'

        return result

    def create_token(self, device_code):
        data = {'grant_type': self.grant_type, 'code': device_code}

        response = self.auth_request(data)

        return self.add_expires(json.loads(response))

    def update_token(self, refresh_token):
        data = {'grant_type': 'refresh_token', 'refresh_token': refresh_token}

        response = self.auth_request(data)

        return self.add_expires(json.loads(response))

    def auth_request(self, data, rtype='token', method=None):
        data['client_id'] = self.client_id

        if rtype == 'token':
            data['client_secret'] = self.client_secret

        url = self.auth_url + rtype

        return self.http_request(url, data=data, method=method)

    def add_expires(self, data):
        if 'expires_in' in data:
            data['expires'] = int(time.time()) + int(data['expires_in'])

        return data