import json
import common
import pagination
import bookmarks
import sorting
import urllib

@route('/video/etvnet/archive_menu')
def GetArchiveMenu():
    oc = ObjectContainer(title2=unicode(L('Archive')))

    oc.add(DirectoryObject(key=Callback(GetChannels), title=unicode(L('Channels'))))

    result = video_service.get_genres()

    for genre in result['data']:
        key = Callback(HandleGenre, id=genre['id'], name=genre['name'])
        title = genre['name']

        oc.add(DirectoryObject(key=key, title=title))

    oc.add(InputDirectoryObject(key=Callback(SearchMovies), title=unicode(L("Movies Search")), thumb=R(SEARCH_ICON)))

    return oc

@route('/video/etvnet/search_movies')
def SearchMovies(query=None, page=1, **params):
    response = video_service.search(query=query, per_page=common.get_elements_per_page(), page=page)

    oc = ObjectContainer(title2=unicode(L('Movies Search')))

    for media in HandleMediaList(response['data']['media']):
        oc.add(media)

    pagination.append_controls(oc, response, page=page, callback=SearchMovies, query=query)

    if len(oc) < 1:
        return common.no_contents('Movies Search')

    return oc

@route('/video/etvnet/topics_menu')
def GetTopicsMenu():
    oc = ObjectContainer(title2=unicode(L('Topics')))

    for topic in video_service.TOPICS:
        oc.add(DirectoryObject(
            key=Callback(HandleTopic, id=topic),
            title=unicode(L(topic))
        ))

    return oc

@route('/video/etvnet/topic')
def HandleTopic(id, page=1, **params):
    oc = ObjectContainer(title2=unicode(L(id)))

    response = video_service.get_topic_items(id, page=page)

    for media in HandleMediaList(response['data']['media']):
        oc.add(media)

    pagination.append_controls(oc, response, callback=HandleTopic, id=id, page=page)

    return oc

@route('/video/etvnet/channels')
def GetChannels():
    oc = ObjectContainer(title2=unicode(L('Channels')))

    response = video_service.get_channels()

    for channel in response['data']:
        key = Callback(HandleChannel, id=channel['id'], name=channel['name'])
        title = unicode(channel['name'])

        oc.add(DirectoryObject(key=key, title=title))

    return oc

@route('/video/etvnet/channel')
def HandleChannel(id, name, page=1, **params):
    oc = ObjectContainer(title2=unicode(name))

    response = video_service.get_archive(channel_id=id, per_page=common.get_elements_per_page(), page=page)

    for media in HandleMediaList(response['data']['media']):
        oc.add(media)

    pagination.append_controls(oc, response, page=page, callback=HandleChannel, id=id, name=name)

    return oc

@route('/video/etvnet/genre')
def HandleGenre(id, name, page=1, **params):
    oc = ObjectContainer(title2=unicode(name))

    response = video_service.get_archive(genre=int(id), per_page=common.get_elements_per_page(), page=page)

    for media in HandleMediaList(response['data']['media']):
        oc.add(media)

    pagination.append_controls(oc, response, page=page, callback=HandleGenre, id=id, name=name)

    return oc

@route('/video/etvnet/new_arrivals')
def GetNewArrivals(page=1, **params):
    oc = ObjectContainer(title2=unicode(L('New Arrivals')))

    response = video_service.get_new_arrivals(per_page=common.get_elements_per_page(), page=page)

    for media in HandleMediaList(response['data']['media']):
        oc.add(media)

    pagination.append_controls(oc, response, page=page, callback=GetNewArrivals)

    return oc

@route('/video/etvnet/history')
def GetHistory(page=1, **params):
    oc = ObjectContainer(title2=unicode(L('History')))

    response = video_service.get_history(per_page=common.get_elements_per_page(), page=page)

    for media in HandleMediaList(response['data']['media']):
        oc.add(media)

    pagination.append_controls(oc, response, page=page, callback=GetHistory)

    return oc

def HandleMediaList(response, in_queue=False):
    list = []

    for media in response:
        type = media['type']
        id = media['id']
        name = media['name']
        thumb = media['thumb']

        if type == 'Container':
            key = Callback(HandleChildren, id=id, name=name, thumb=thumb, in_queue=in_queue)

            list.append(DirectoryObject(key=key, title=name, thumb=thumb))
        else:
            if type == 'MediaObject':
                key = Callback(HandleChild,
                    id = id,
                    name = name,
                    thumb = thumb,
                    rating_key = media['rating'],
                    description = media['description'],
                    duration = media['duration'],
                    year = media['year'],
                    on_air = media['on_air'],
                    index = media['series_num'],
                    files = json.dumps(media['files']
                ))

                watch_status = media['watch_status']

                if watch_status == 1:
                    name = "~ " + name
                elif watch_status == 2:
                    name = "* " + name

                list.append(DirectoryObject(key=key, title=name, thumb=thumb))

    return list

@route('/video/etvnet/children')
def HandleChildren(id, name, thumb, in_queue=False, page=1, dir='desc'):
    oc = ObjectContainer(title2=unicode(name))

    response = video_service.get_children(int(id), per_page=common.get_elements_per_page(), page=page, dir=dir)

    for media in HandleMediaList(response['data']['children'], in_queue=in_queue):
        oc.add(media)

    bookmarks.append_controls(oc, id=id, name=name, thumb=thumb)
    sorting.append_controls(oc, HandleChildren, id=id, name=name, thumb=thumb, in_queue=in_queue, page=page, dir=dir)

    pagination.append_controls(oc, response, callback=HandleChildren, id=id, name=name, thumb=thumb,
                               in_queue=in_queue, page=page, dir=dir)

    return oc

@route('/video/etvnet/child')
def HandleChild(id, name, thumb, rating_key, description, duration, year, on_air, index, files, container=False):
    oc = ObjectContainer(title2=unicode(name))

    oc.add(GetVideoObject(id, 'movie', name, thumb, rating_key, description, duration, year, on_air, index, files, container))

    if str(container) == 'False':
        bookmarks.append_controls(oc, id=id, name=name, thumb=thumb, rating_key=rating_key,
            description=description, duration=duration, year=year, on_air=on_air, files=files, container=container)

    return oc

def GetVideoObject(id, media_type, name, thumb, rating_key, description, duration, year, on_air, index, files, container):
    video = build_metadata_object(media_type=media_type, name=name, year=year, index=index)

    video.rating_key = rating_key
    video.thumb = thumb
    video.duration = int(duration)*60*1000
    video.summary = unicode(description)
    video.originally_available_at = originally_available_at(on_air)

    video.key = Callback(HandleChild, id=id, name=name, thumb=thumb,
                         rating_key=rating_key, description=description, duration=duration, year=year,
                         on_air=on_air, index=index, files=files, container=True)

    files = json.loads(urllib.unquote_plus(files))

    video.items = []

    for format, bitrates in video_service.bitrates(files, common.get_format(), common.get_quality_level()).iteritems():
        video.items.extend(MediaObjectsForURL(id=id, format=str(format), bitrates=json.dumps(bitrates)))

    return video

def build_metadata_object(media_type, name, year, index=None):
    if media_type == 'episode':
        video = EpisodeObject(show=name, index=int(index))
    elif media_type == 'movie':
        #video = MovieObject(title=name, year=int(year))
        video = VideoClipObject(title=name, year=int(year))
    else:
        video = VideoClipObject(title=name, year=int(year))

    return video

def MediaObjectsForURL(id, format, bitrates):
    media_objects = []

    for bitrate in sorted(json.loads(bitrates), reverse=True):
        media_object = MediaObject(
            protocol = Protocol.HLS,
            container=Container.MP4,
            optimized_for_streaming=True
        )

        audio_stream = AudioStreamObject(
            codec=AudioCodec.AAC,
            channels=2,
            bitrate=str(bitrate)
        )

        video_stream = VideoStreamObject(
            codec=VideoCodec.H264
        )

        key = Callback(PlayVideo, id=id, format=format, bitrate=str(bitrate))

        part_object = PartObject(
            key = key,
            streams = [audio_stream, video_stream]
        )

        media_object.parts = [part_object]

        media_objects.append(media_object)

    return media_objects

def originally_available_at(on_air):
    return Datetime.ParseDate(on_air.replace('+', ' ')).date()

@indirect
@route('/video/etvnet/play_video')
def PlayVideo(id, bitrate, format, **params):
    response = video_service.get_url(media_id=id, format=format, bitrate=bitrate, other_server=common.other_server())

    url = response['url']

    if not url:
        common.no_contents()
    else:
        return IndirectResponse(MovieObject, key=HTTPLiveStreamURL(url))

