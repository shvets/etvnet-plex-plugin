import json
import datetime
import urllib

import common
import pagination
import archive

@route('/video/etvnet/live_channels_menu')
def GetLiveChannelsMenu():
    def _():
        oc = ObjectContainer(title2=unicode(L('Live')))

        oc.add(DirectoryObject(key=Callback(GetLiveChannels, title=L('All Channels')),title=unicode(L('All Channels'))))
        oc.add(DirectoryObject(key=Callback(GetLiveChannels, title=L('Favorite'), favorite_only=True), title=unicode(L('Favorite'))))

        # oc.add(DirectoryObject(key=Callback(GetLiveGenres, title=L('Genres')), title=unicode(L('Genres'))))

        result = video_service.get_live_categories()

        for genre in result['data']:
            name = genre['name']
            category = int(genre['id'])

            oc.add(DirectoryObject(
                key=Callback(GetLiveChannels, title=name, category=category),
                title=unicode(name)
            ))

        return oc

    return video_service.error_handler.handle_exception(_)

@route('/video/etvnet/live_channels')
def GetLiveChannels(title, favorite_only=False, category=0, page=1, **params):
    page = int(page)

    def _():
        oc = ObjectContainer(title2=unicode(title))

        response = video_service.get_live_channels(favorite_only=favorite_only, category=category)

        for index, media in enumerate(response['data']):
            if index >= (page-1)*common.get_elements_per_page() and index < page*common.get_elements_per_page():
                id = media['id']
                name = media['name']
                thumb = media['icon']
                files = media['files']

                oc.add(DirectoryObject(
                    key=Callback(GetLiveChannel, name=name, channel_id=id, thumb=thumb, files=json.dumps(files)),
                    title=unicode(name),
                    thumb=Resource.ContentsOfURLWithFallback(url=thumb)
                ))

        add_pagination_to_response(response, page)
        pagination.append_controls(oc, response, callback=GetLiveChannels, title=title, favorite_only=favorite_only, page=page)

        return oc

    return video_service.error_handler.handle_exception(_)

@route('/video/etvnet/live_channel')
def GetLiveChannel(name, channel_id, thumb, files, container=False):
    def _():
        oc = ObjectContainer(title2=unicode(name))

        oc.add(MetadataObjectForURL(name, channel_id, thumb, files, container))

        if not container:
            oc.add(DirectoryObject(key=Callback(GetSchedule, channel_id=channel_id), title=unicode(L('Schedule'))))

            append_controls(oc, id=channel_id, name=name, thumb=thumb)

        return oc

    return video_service.error_handler.handle_exception(_)

def MetadataObjectForURL(name, channel_id, thumb, files, container):
    video = MovieObject(
        rating_key='rating_key',
        title=unicode(name),
        thumb=Resource.ContentsOfURLWithFallback(url=thumb)
    )

    offset = video_service.get_offset(common.get_time_shift())

    format ='mp4'

    new_files = json.loads(urllib.unquote_plus(files))

    bitrates = video_service.bitrates(new_files, accepted_format=format, quality_level=common.get_quality_level())

    video.key = Callback(GetLiveChannel, name=name, channel_id=channel_id, thumb=thumb, files=files, container=True)
    video.items = MediaObjectsForURL(channel_id=channel_id, format=format, offset=offset, bitrates=json.dumps(bitrates[format]))

    return video

@route('/video/etvnet/schedule')
def GetSchedule(channel_id):
    oc = ObjectContainer(title2=unicode(L('Schedule')))

    default_time = get_moscow_time()

    today = default_time.date()

    yesterday = today - datetime.timedelta(days=1)
    tomorrow = today + datetime.timedelta(days=1)

    yesterday_result = video_service.get_live_schedule(live_channel_id=channel_id, date=yesterday)
    today_result = video_service.get_live_schedule(live_channel_id=channel_id, date=today)
    tomorrow_result = video_service.get_live_schedule(live_channel_id=channel_id, date=tomorrow)

    add_schedule(oc, channel_id, default_time, yesterday_result['data'])
    add_schedule(oc, channel_id, default_time, today_result['data'])
    add_schedule(oc, channel_id, default_time, tomorrow_result['data'])

    return oc

def add_schedule(oc, channel_id, default_time, list):
    channels = video_service.get_live_channels()['data']

    channel = find_channel(int(channel_id), channels)

    offset = video_service.get_offset(common.get_time_shift())
    time_delta = datetime.timedelta(hours=offset)

    files = channel['files']

    for media in list:
        start_time = get_time(media['start_time'])
        finish_time = get_time(media['finish_time'])

        current_title = in_time_range(default_time - time_delta, start_time, finish_time)

        if media['media_id']:
            if media['rating']:
                rating = media['rating']
            else:
                rating = 'unknown'

            key = Callback(archive.HandleChild,
                id = media['media_id'],
                name = media['name'],
                # thumb = 'thumb',
                rating_key = rating,
                description = media['description'],
                # duration = 0,
                # year = 0,
                on_air = media['start_time'],
                files = json.dumps(files)
            )

            title = get_schedule_title(media['name'], start_time, finish_time, current_title=current_title)

            oc.add(DirectoryObject(key=key, title=unicode(title)))
        else:
            select_key = Callback(GetSchedule, channel_id=channel_id)

            title = get_schedule_title(media['name'], start_time, finish_time, current_title=current_title, available=False)

            oc.add(DirectoryObject(key=select_key, title=unicode(title)))

def in_time_range(actual_time, start_time, finish_time):
    in_range = False

    if actual_time.day == start_time.day:
        if actual_time.hour == finish_time.hour:
            if actual_time.minute <= finish_time.minute:
                in_range = True
        elif actual_time.hour == start_time.hour:
            if actual_time.minute >= start_time.minute:
                return True

    return in_range

def get_schedule_title(name, start_time, finish_time, current_title=False, available=True):
    if current_title:
        left_sep = "---> "
        right_sep = " <---"
    else:
        left_sep = ""
        right_sep = ""

    if not available:
        left_sep = left_sep  + " ***"
        right_sep = right_sep + " ***"

    prefix = str(start_time)[11:16] + " - " + str(finish_time)[11:16] + " : "

    return prefix + left_sep + name + right_sep

def get_time(value):
    return datetime.datetime.strptime(value.replace('T', ' '), '%Y-%m-%d %H:%M:%S')

def get_moscow_time():
    utc_datetime = datetime.datetime.utcnow()

    time = datetime.datetime.strptime(str(utc_datetime), '%Y-%m-%d %H:%M:%S.%f')

    return time + datetime.timedelta(hours=3)

#RAW_HLS_CLIENTS = ['Android', 'iOS', 'Roku', 'Safari']
# if Client.Platform in RAW_HLS_CLIENTS:
#if Client.Product in ['Plex Web', 'Plex for Xbox One'] and not Client.Platform == 'Safari':
#    Log(Client.Platform)
#    Log(Client.Product)
# Plex for iOS
# Plex Web
# Plex for Apple TV
#'iOS' 'tvOS'

def MediaObjectsForURL(channel_id, format, offset, bitrates):
    media_objects = []

    #for video_resolution in ['1080', '720', '540', '360', '240']:
    #resolution = ['720', '360', '360', '360']
    video_resolution = '720'

    for bitrate in sorted(json.loads(bitrates), reverse=True):
        if Client.Product == 'Plex Web':
            media_object =  MediaObject(
                protocol='hls',
                container = 'mpegts',

                # video_resolution = video_resolution,
                optimized_for_streaming = False
            )

            # key = Callback(PlayIndirectHLS, channel_id=channel_id, bitrate=str(bitrate), format=format, offset=offset)
            #
            # part_object = PartObject(key=key)

            audio_stream = AudioStreamObject(
                codec = AudioCodec.AAC,
                channels = 2,
                bitrate=str(bitrate)
            )

            video_stream = VideoStreamObject(
                codec=VideoCodec.H264
                #codec=Container.MP4
            )

            key = Callback(PlayIndirectHLS, channel_id=channel_id, bitrate=str(bitrate), format=format, offset=offset)

            part_object = PartObject(
                key=key,
                streams = [audio_stream, video_stream]
            )
        elif Client.Platform in ['iOS', 'Safari', 'tvOS']:
            media_object = MediaObject(
                video_resolution = 720,
                audio_channels = 2,
                optimized_for_streaming = True
            )

            key = Callback(PlayIndirectHLS, channel_id=channel_id, bitrate=str(bitrate), format=format, offset=offset)

            part_object = PartObject(key=key)
        else:
            media_object = MediaObject(
                #video_resolution = video_resolution,
                #video_resolution = 288,
                # video_frame_rate='',
                # duration=0,
                # height='',
                # width='',
                # video_resolution = '720',
                # aspect_ratio = '1.78',

                protocol='hls',
                container = 'mpegts',

                optimized_for_streaming=True
            )

            audio_stream = AudioStreamObject(
                codec = AudioCodec.AAC,
                channels = 2,
                bitrate=str(bitrate)
            )

            video_stream = VideoStreamObject(
                codec=VideoCodec.H264
                #codec=Container.MP4
            )

            key = Callback(PlayIndirectHLS, channel_id=channel_id, bitrate=str(bitrate), format=format, offset=offset)

            part_object = PartObject(
                key=key,
                streams = [audio_stream, video_stream]
            )

        media_object.parts = [part_object]

        media_objects.append(media_object)

    return media_objects

@indirect
@route('/video/etvnet/play_indirect_hls')
def PlayIndirectHLS(channel_id, bitrate, format, offset, **params):
    response = video_service.get_url(None, channel_id=channel_id, bitrate=bitrate, format=format, live=True,
                               offset=offset, other_server=common.other_server())

    Log(response['url'])

    if not response['url']:
        #common.no_contents()
        raise Ex.MediaNotAvailable
    else:
        return IndirectResponse(VideoClipObject, key=HTTPLiveStreamURL(response['url']))

# @route('/video/etvnet/play_direct_hls')
# def PlayDirectHLS(channel_id, bitrate, format, offset, **params):
#     response = video_service.get_url(None, channel_id=channel_id, bitrate=bitrate, format=format, live=True, offset=offset)
#
#     Log(response['url'])
#
#     if not response['url']:
#         common.no_contents()
#     else:
#         return Redirect(
#             Callback(CreatePatchedPlaylist, url = response['url'], cookies = HTTP.CookiesForURL(response['url'])))

# USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/600.3.18 (KHTML, like Gecko) Version/8.0.3 Safari/600.3.18'
#
# @route('/video/etvnet/patched_playlist')
# def CreatePatchedPlaylist(url, cookies):
#     headers               = {}
#     headers['Cookie']     = cookies
#     headers['User-Agent'] = USER_AGENT
#
#     original_playlist = HTTP.Request(url, headers = headers, cacheTime = 0).content
#
#     path = url[ : url.rfind('/') + 1]
#
#     new_playlist = ''
#
#     for line in original_playlist.splitlines():
#         if line.startswith('#EXT-X-KEY'):
#             original_key_url = RE_KEY_URI.search(line).groups()[0]
#             new_key_url = Callback(ContentOfURL, url = original_key_url, cookies = cookies)
#             new_playlist = new_playlist + line.replace(original_key_url, new_key_url) + '\n'
#         elif line.startswith('http'):
#             original_segment_url = line
#             new_segment_url = Callback(ContentOfURL, url = original_segment_url, cookies = cookies)
#             new_playlist = new_playlist + new_segment_url + '\n'
#         elif '.ts' in line:
#             original_segment_url = line
#             new_segment_url = Callback(ContentOfURL, url = path + original_segment_url, cookies = cookies)
#             new_segment_url = 'http://' + Network.Address + ':32400' + new_segment_url
#             new_playlist = new_playlist + new_segment_url + '\n'
#         else:
#             new_playlist = new_playlist + line + '\n'
#
#     return new_playlist
#
# @route('/video/etvnet/content_of_url')
# def ContentOfURL(url, cookies):
#     headers               = {}
#     headers['Cookie']     = cookies
#     headers['User-Agent'] = USER_AGENT
#
#     return HTTP.Request(url, headers = headers, cacheTime = 0).content


def append_controls(oc, **params):
    favorite_channels = video_service.get_live_channels(favorite_only=True)['data']

    favorite_channel = find_channel(int(params['id']), favorite_channels)

    if favorite_channel:
        oc.add(DirectoryObject(
                key=Callback(HandleRemoveFavoriteChannel, type=type, **params),
                title=unicode(L('Remove Favorite')),
                thumb=R(REMOVE_ICON)
        ))
    else:
        oc.add(DirectoryObject(
                key=Callback(HandleAddFavoriteChannel, type=type, **params),
                title=unicode(L('Add Favorite')),
                thumb=R(ADD_ICON)
        ))

def find_channel(id, favorite_channels):
    found = None

    for media in favorite_channels:
        if id == media['id']:
            found = media
            break

    return found

@route('/video/etvnet/add_favorite_channel')
def HandleAddFavoriteChannel(**params):
    video_service.add_favorite_channel(params['id'])

    return ObjectContainer(header=unicode(L(params['name'])), message=unicode(L('Favorite Added')))

@route('/video/etvnet/remove_favorite_channel')
def HandleRemoveFavoriteChannel(**params):
    video_service.remove_favorite_channel(params['id'])

    return ObjectContainer(header=unicode(L(params['name'])), message=unicode(L('Favorite Removed')))

def add_pagination_to_response(response, page):
    pages = len(response['data'])/common.get_elements_per_page()

    response['data'] = {'pagination': {
        'page': page,
        'pages': pages,
        'has_next': page < pages,
        'has_previous': page > 1
    }}