# coding=utf-8

import time
from datetime import date

from api_service import ApiService

class EtvnetService(ApiService):
    PER_PAGE = 15

    API_URL = 'https://secure.etvnet.com/api/v3.0/'
    USER_AGENT = 'Plex User Agent'

    AUTH_URL = 'https://accounts.etvnet.com/auth/oauth/'
    CLIENT_ID = "a332b9d61df7254dffdc81a260373f25592c94c9"
    CLIENT_SECRET = '744a52aff20ec13f53bcfd705fc4b79195265497'

    SCOPE = (
        'com.etvnet.media.browse '
        'com.etvnet.media.watch '
        'com.etvnet.media.bookmarks '
        'com.etvnet.media.history '
        'com.etvnet.media.live '
        'com.etvnet.media.fivestar '
        'com.etvnet.media.comments '
        'com.etvnet.persons '
        'com.etvnet.notifications '
    )

    GRANT_TYPE = 'http://oauth.net/grant_type/device/1.0'

    TIME_SHIFT = {
        0: 0,  # Moscow
        1: 2,  # Berlin
        2: 3,  # London
        3: 8,  # New York
        4: 9,  # Chicago
        5: 10, # Denver
        6: 11  # Los Angeles
    }

    TOPICS = ["etvslider/main", "newmedias", "best", "top", "newest", "now_watched", "recommend"]

    def __init__(self, config):
        self.last_url_requested = None

        ApiService.__init__(self, config, self.API_URL, self.USER_AGENT, self.AUTH_URL, self.CLIENT_ID,
                            self.CLIENT_SECRET, self.GRANT_TYPE, self.SCOPE)

    def on_authorization_success(self, user_code, device_code, activation_url):
        print("Register activation code on web site (" + activation_url + "): " + user_code)

        response = None

        done = False

        while not done:
            response = self.create_token(device_code=device_code)

            if response:
                done = response.has_key('access_token')

            if not done:
                time.sleep(5)

        self.config.save(response)

        return response

    def get_url(self, media_id, format='mp4', protocol='hls', bitrate=None, other_server=None, offset=None,
                live=False, channel_id=None, preview=False):
        if format == 'zixi':
            format = 'mp4'

        if live:
            # if format == 'mp4':
            #     protocol = 'hls'

            path = 'video/live/watch/%d.json?' % int(channel_id)

            params = {"offset": offset, "format": format, "bitrate": bitrate, "other_server": other_server}
        else:
            if format == 'wmv':
                protocol = None

            if format == 'mp4' and protocol is None:
                protocol = 'rtmp'

            if preview:
                link_type = 'preview'
            else:
                link_type = 'watch'

            path = 'video/media/%d/%s.json?' % (int(media_id), link_type)

            params = {"format": format, "protocol": protocol, "bitrate": bitrate, "other_server": other_server}

        path = self.build_url(path, **params)

        result = self.full_request(path)

        print(result)

        if result:
          return {"url": result['data']['url'], "protocol": protocol, "format": format, "bitrate": bitrate}
        else:
            return {"url": None, "protocol": None, "format": None, "bitrate": None}

    def bitrates(self, data, accepted_format=None, quality_level=None):
        bitrates = {}

        for pair in data:
            format = pair['format']
            bitrate = pair['bitrate']

            if not accepted_format or accepted_format == format:
                if not format in bitrates.keys():
                    bitrates[format] = []

                bitrates[format].append(bitrate)

        for key in bitrates.keys():
            bitrates[key] = self.filtered(sorted(bitrates[key], reverse=True), quality_level)

        return bitrates

    def get_offset(self, shift):
        return self.TIME_SHIFT.get(shift, 0)

    def filtered(self, bitrates, quality_level):
        if quality_level == None:
            return bitrates
        else:
            # Best, High, Medium, Low, Undefined
            filter_map = {
                1: [0, 0, 0, 0],
                2: [1, 0, 0, 0],
                3: [2, 1, 0, 0],
                4: [3, 2, 1, 0]
            }

            index = filter_map[len(bitrates)][quality_level-1]

            return [bitrates[index]]

    def get_archive(self, genre=None, channel_id=None, per_page=PER_PAGE, page=1, **params):
        if channel_id and genre:
            path = 'video/media/channel/%d/archive/%d.json' % (int(channel_id), int(genre))
        elif genre:
            path = 'video/media/archive/%d.json' % int(genre)
        elif channel_id:
            path = 'video/media/channel/%d/archive.json' % int(channel_id)
        else:
            path = 'video/media/archive.json'

        url = self.build_url(path, per_page=per_page, page=page, **params)

        self.last_url_requested = url

        return self.full_request(url)

    def get_channels(self, today=False):
        path = 'video/channels.json'
        # today = (None, 'yes')[today is True]

        return self.full_request(self.build_url(path, today=today))

    def get_children(self, media_id, per_page=PER_PAGE, page=1, dir=None):
        path = 'video/media/%d/children.json' % media_id
        url = self.build_url(path, per_page=per_page, page=page, dir=dir)

        self.last_url_requested = url

        return self.full_request(url)

    def get_genres(self, parent_id=None, today=False, channel_id=None, format=None):
        path = 'video/genres.json'
        today = (None, 'yes')[today is True]

        url = self.build_url(path, parent=parent_id, today=today, channel=channel_id, format=format)

        result = self.full_request(url)

        # regroup genres

        data = result['data']

        genres = []

        genres.append(data[0])
        genres.append(data[1])
        genres.append(data[5])
        genres.append(data[9])
        genres.append(data[7])
        genres.append(data[2])
        genres.append(data[3])
        genres.append(data[4])
        genres.append(data[6])
        genres.append(data[8])
        genres.append(data[10])
        genres.append(data[11])
        genres.append(data[12])
        #genres.append(data[13])
        genres.append(data[14])
        #genres.append(data[15])

        result['data'] = genres

        return result

    def get_genre(self, genres, name):
        genre = None

        for item in genres['data']:
            if item['name'].encode('utf-8') == name:
                genre = item['id']
                break

        return genre

    def get_blockbusters(self, per_page=PER_PAGE, page=1, **params):
        genres = self.get_genres()

        genre = self.get_genre(genres, "Блокбастеры")

        return self.get_archive(genre=genre, per_page=per_page, page=page, **params)

    def get_for_kids(self, per_page=PER_PAGE, page=1):
        genres = self.get_genres()

        genre = self.get_genre(genres, "Детям")

        return self.get_archive(genre=genre, per_page=per_page, page=page)

    def search(self, query, per_page=PER_PAGE, page=1, dir=None):
        if not dir:
            dir = 'desc'

        path = 'video/media/search.json'

        return self.full_request(self.build_url(path, q=query, per_page=per_page, page=page, dir=dir))

    def get_new_arrivals(self, genre=None, channel_id=None, per_page=PER_PAGE, page=1):
        if channel_id and genre:
            path = 'video/media/channel/%d/new_arrivals/%d.json' % (int(channel_id), genre)
        elif genre:
            path = 'video/media/new_arrivals/%d.json' % genre
        elif channel_id:
            path = 'video/media/channel/%d/new_arrivals.json' % int(channel_id)
        else:
            path = 'video/media/new_arrivals.json'

        url = self.build_url(path, per_page=per_page, page=page)

        return self.full_request(url)

    def get_sorted_by(self, field):
        url = self.last_url_requested

        url.params['order_by'] = field

        return self.full_request(url)

    def get_by_letter(self, letter):
        url = self.last_url_requested

        url.params['order_by'] = 'simple_name'
        url.params['first_letter'] = letter

        return self.full_request(url)

    def get_history(self, per_page=PER_PAGE, page=1):
        url = self.build_url('video/media/history.json', per_page=per_page, page=page)

        self.last_url_requested = url

        return self.full_request(url)

    def get_bookmark(self, id):
        return self.full_request(self.build_url('video/bookmarks/items/%d.json' % int(id)), method='GET')

    def add_bookmark(self, id):
        return self.full_request(self.build_url('video/bookmarks/items/%d.json' % int(id)), method='POST')

    def remove_bookmark(self, id):
        return self.full_request(self.build_url('video/bookmarks/items/%d.json' % int(id)), method='DELETE')

    def get_bookmarks(self, folder=None, per_page=PER_PAGE, page=None):
        if folder:
            params = {"per_page": per_page, "page": page}

            path = 'video/bookmarks/folders/%s/items.json' % folder
        else:
            params = {"per_page": per_page, "page": page}

            path = 'video/bookmarks/items.json'

        return self.full_request(self.build_url(path, **params))

    def add_favorite_channel(self, id):
        path = 'video/live/%d/favorite.json' % int(id)

        return self.full_request(self.build_url(path), method='POST')

    def remove_favorite_channel(self, id):
        path = 'video/live/%d/favorite.json' % int(id)

        return self.full_request(self.build_url(path), method='DELETE')

    def get_live_channels(self, favorite_only=None, offset=None, category=0):
        format = 'mp4'

        params = {"format": format, "allowed_only": 1, "favorite_only": favorite_only, "offset": offset}

        if category:
            return self.full_request(self.build_url('video/live/category/%d.json?' % int(category), **params))
        else:
            return self.full_request(self.build_url('video/live/channels.json', **params))

    def get_live_schedule(self, live_channel_id, date=date.today()):
        url = self.build_url("video/live/schedule/%d.json" % int(live_channel_id), date=date)

        return self.full_request(url)

    def get_live_categories(self):
        url = self.build_url("video/live/category.json")

        result = self.full_request(url)

        # regroup categories

        data = result['data']

        categories = []

        categories.append(data[8])
        categories.append(data[6])
        categories.append(data[3])
        categories.append(data[2])
        categories.append(data[1])
        categories.append(data[5])
        categories.append(data[7])
        categories.append(data[0])
        categories.append(data[4])

        result['data'] = categories

        return result

    def get_topic_items(self, id='best', per_page=PER_PAGE, page=None):
        params = {"per_page": per_page, "page": page}

        url = self.build_url("video/media/%s.json" % id, **params)

        return self.full_request(url)

    def get_folders(self, per_page=PER_PAGE):
        params = {"per_page": per_page}

        return self.full_request('video/bookmarks/folders.json', **params)
