import test_helper

import unittest

import json
from config import Config
from etvnet_service import EtvnetService

class EtvnetAuthServiceTest(unittest.TestCase):
    def setUp(self):
        config = Config("../etvnet.config")

        self.service = EtvnetService(config)

    def test_get_activation_codes(self):
        result = self.service.get_activation_codes()

        activation_url = result['activation_url']
        user_code = result['user_code']
        device_code = result['device_code']

        print("Activation url: " + activation_url)
        print("Activation code: " + user_code)

        self.assertNotEqual(device_code, None)
        self.assertNotEqual(user_code, None)

    def test_create_token(self):
        response = self.service.authorization()

        self.assertNotEqual(response['access_token'], None)
        self.assertNotEqual(response['refresh_token'], None)

    def test_update_token(self):
        refresh_token = self.service.config.get_value('refresh_token')

        response = self.service.update_token(refresh_token)

        self.service.config.save(response)

        print(json.dumps(response, indent=4))

        self.assertNotEqual(response['access_token'], None)
        self.assertNotEqual(response['refresh_token'], None)

    def test_complete_request(self):
        result = self.service.get_channels()

        print(json.dumps(result, indent=4))

if __name__ == '__main__':
    unittest.main()
