import time

import json

from urllib2 import HTTPError

try:
    from urlparse import urljoin
except:
    from urllib.parse import urljoin

from auth_service import AuthService

class ApiService(AuthService):
    def __init__(self, config, api_url, user_agent, auth_url, client_id, client_secret, grant_type, scope):
        self.config = config
        self.config.load()

        self.api_url = api_url
        self.user_agent = user_agent

        AuthService.__init__(self, auth_url, client_id, client_secret, grant_type, scope)

    def reset_token(self):
        if 'access_token' in self.config.config:
            del self.config.config['access_token']

        if 'refresh_token' in self.config.config:
            del self.config.config['refresh_token']

        if 'device_code' in self.config.config:
            del self.config.config['device_code']

        self.config.save()

    def api_request(self, base_url, path, method=None, headers=None, data=None, *a, **k):
        if not headers:
            headers = {}

        url = urljoin(base_url, path)

        if not headers:
            headers = {}

        headers['User-agent'] = self.user_agent

        return self.http_request(url, headers=headers, data=data, method=method)

    def authorization(self, on_authorization_success=None, on_authorization_failure=None, include_client_secret=True):
        if not on_authorization_success:
            on_authorization_success = self.on_authorization_success

        if not on_authorization_failure:
            on_authorization_failure = self.on_authorization_failure

        if self.check_access_data('device_code'):
            activation_url = self.config.config['activation_url']
            user_code = self.config.config['user_code']
            device_code = self.config.config['device_code']
        else:
            ac_response = self.get_activation_codes(include_client_secret=include_client_secret)

            activation_url = ac_response['activation_url']
            user_code = ac_response['user_code']
            device_code = ac_response['device_code']

            self.config.save({
                "user_code": unicode(user_code),
                "device_code": unicode(device_code),
                "activation_url": unicode(activation_url)
            })

        if user_code:
            result = on_authorization_success(user_code, device_code, activation_url)
        else:
            result = on_authorization_failure()

        return result

    def on_authorization_success(self, user_code, device_code, activation_url):
        return None

    def on_authorization_failure(self):
        return None

    def check_access_data(self, key):
        if key == 'device_code':
            return key in self.config.config
        else:
            return (key in self.config.config and
                    'expires' in self.config.config and self.config.config['expires'] >= int(time.time()))

    def check_token(self):
        try:
            if self.check_access_data('access_token'):
                return True

            elif 'refresh_token' in self.config.config:
                refresh_token = self.config.get_value('refresh_token')

                response = self.update_token(refresh_token)

                self.config.save(response)

                return True

            elif self.check_access_data('device_code'):
                device_code = self.config.config['device_code']

                response = self.create_token(device_code=device_code)

                response['device_code'] = device_code

                self.config.save(response)

                # return True

            return False
        except HTTPError as e:
            if e.code == 400:
                self.reset_token()
            return False

    def full_request(self, path, method=None, data=None, unauthorized=False, *a, **k):
        if not self.check_token():
            self.authorization()

        response = None

        try:
            access_token = self.config.get_value('access_token')

            access_path = path + ('?', '&')['?' in path] + 'access_token=%s' % access_token

            response = self.api_request(self.api_url, access_path, method, data, *a, **k)

            if len(response) > 0:
                response = json.loads(response)
        except HTTPError as e:
            if e.code == 401 and not unauthorized:
                #or e.code == 400:
                refresh_token = self.config.get_value('refresh_token')

                response = self.update_token(refresh_token)

                if response:
                    self.config.save(response)

                    response = self.full_request(path, method, data, unauthorized=True, *a, **k)
                else:
                    print('error')
            else:
                print(e)

        return response
