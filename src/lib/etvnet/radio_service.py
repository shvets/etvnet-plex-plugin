# -*- coding: utf-8 -*-

import json

from http_service import HttpService

class RadioService(HttpService):
    RADIO_URL = "http://radio.etvnet.com/station"

    USER_AGENT = 'Plex User Agent'

    STATIONS = [
        {'id': 14, 'name': "Радио \"Диско СССР\""},
        {'id': 15, 'name': "Радио \"Русский Хит\""},
        {'id': 18, 'name': "Радио \"Детский Мир\""},
        {'id': 33, 'name': "Радио \"Барды\""},
        {'id': 34, 'name': "Радио \"Музыка Кино и ТВ\""},
        {'id': 36, 'name': "Радио \"Шансон\""}
    ]

    def get_stations(self):
        return self.STATIONS

    def get_station(self, id):
        headers = {}
        headers['User-agent'] = self.USER_AGENT
        #headers['Content-Type'] = 'application/json'

        url = self.RADIO_URL + "/" + str(id)

        return json.loads(self.http_request(url, headers=headers))

