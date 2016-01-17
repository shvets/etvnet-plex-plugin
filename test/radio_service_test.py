import test_helper

import unittest
import json

from etvnet_radio_service import EtvnetRadioService

class RadioServiceTest(unittest.TestCase):
    def setUp(self):
        self.service = EtvnetRadioService()

    def test_get_stations(self):
        result = self.service.get_stations()

        print(json.dumps(result, indent=4))

    def test_get_station(self):
        result = self.service.get_station(36)

        print(json.dumps(result, indent=4))

if __name__ == '__main__':
    unittest.main()