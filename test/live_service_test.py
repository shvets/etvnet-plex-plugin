import test_helper

import unittest
from datetime import date

from etvnet_service import EtvnetService
from config import Config

class LiveServiceTest(unittest.TestCase):
    def setUp(self):
        config = Config("../etvnet.config")

        self.service = EtvnetService(config)

    def test_live_channels(self):
        result = self.service.get_live_channels()

        #print(json.dumps(result, indent=4))

        self.assertEqual(result['status_code'], 200)
        self.assertNotEqual(len(result['data']), 0)

        for value in result['data']:
            print(value['id'])
            print(value['name'])
            print(value['icon'])
            print(value['live_format'])
            print(value['files'])

    def test_live_channel(self):
        result = self.service.get_live_channels()

        #print(json.dumps(result, indent=4))

        self.assertEqual(result['status_code'], 200)
        self.assertNotEqual(len(result['data']), 0)

        channel = result['data'][0]

        url_data = self.service.get_url(None, channel_id=channel['id'], bitrate='400', format='mp4', live=True, offset=channel['offset'])

        print(url_data)

        self.assertNotEqual(url_data['url'], None)

    def test_live_schedule(self):
        result = self.service.get_live_channels()
        channel = result['data'][0]

        result = self.service.get_live_schedule(live_channel_id=channel['id'], date=date.today())

        #print(json.dumps(result, indent=4))

        for value in result['data']:
            print(value['rating'])
            print(value['media_id'])
            print(value['name'])
            print(value['finish_time'])
            print(value['start_time'])
            print(value['current_show'])
            print(value['categories'])
            print(value['efir_week'])
            print(value['channel'])
            print(value['description'])

        self.assertEqual(result['status_code'], 200)
        self.assertNotEqual(len(result['data']), 0)

    def test_live_categories(self):
        result = self.service.get_live_categories()

        #print(json.dumps(result, indent=4))

        for value in result['data']:
            print(value['id'])
            print(value['name'])

        self.assertEqual(result['status_code'], 200)
        self.assertNotEqual(len(result['data']), 0)

if __name__ == '__main__':
    unittest.main()