import json
import common
import pagination
import bookmarks
import sorting
import urllib

@route('/video/etvnet/archive_menu')
def GetArchiveMenu():
    def _():
        oc = ObjectContainer(title2=unicode(L('Archive')))

        oc.add(DirectoryObject(key=Callback(GetChannels), title=unicode(L('Channels'))))

        result = video_service.get_genres()

        for genre in result['data']:
            oc.add(DirectoryObject(
                key=Callback(HandleGenre, id=genre['id'], name=genre['name']),
                title=genre['name']
            ))

        oc.add(InputDirectoryObject(key=Callback(SearchMovies), title=unicode(L("Movies Search")), thumb=R(SEARCH_ICON)))

        return oc

    return video_service.error_handler.handle_exception(_)

@route('/video/etvnet/search_movies')
def SearchMovies(query=None, page=1, **params):
    def _():
        response = video_service.search(query=query, per_page=common.get_elements_per_page(), page=page)

        oc = ObjectContainer(title2=unicode(L('Movies Search')))

        for media in HandleMediaList(response['data']['media']):
            oc.add(media)

        pagination.append_controls(oc, response, page=page, callback=SearchMovies, query=query)

        if len(oc) < 1:
            return common.no_contents('Movies Search')

        return oc

    return video_service.error_handler.handle_exception(_)

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
    def _():
        oc = ObjectContainer(title2=unicode(L(id)))

        response = video_service.get_topic_items(id, page=page)

        for media in HandleMediaList(response['data']['media']):
           oc.add(media)

        pagination.append_controls(oc, response, callback=HandleTopic, id=id, page=page)

        return oc

    return video_service.error_handler.handle_exception(_)

@route('/video/etvnet/channels')
def GetChannels():
    def _():
        oc = ObjectContainer(title2=unicode(L('Channels')))

        response = video_service.get_channels()

        for channel in response['data']:
            oc.add(DirectoryObject(
                key=Callback(HandleChannel, id=channel['id'], name=channel['name']),
                title=unicode(channel['name'])
            ))

        return oc

    return video_service.error_handler.handle_exception(_)

@route('/video/etvnet/channel')
def HandleChannel(id, name, page=1, **params):
    def _():
        oc = ObjectContainer(title2=unicode(name))

        response = video_service.get_archive(channel_id=id, per_page=common.get_elements_per_page(), page=page)

        for media in HandleMediaList(response['data']['media']):
           oc.add(media)

        pagination.append_controls(oc, response, page=page, callback=HandleChannel, id=id, name=name)

        return oc

    return video_service.error_handler.handle_exception(_)

@route('/video/etvnet/genre')
def HandleGenre(id, name, page=1, **params):
    def _():
        oc = ObjectContainer(title2=unicode(name))

        response = video_service.get_archive(genre=int(id), per_page=common.get_elements_per_page(), page=page)

        for media in HandleMediaList(response['data']['media']):
           oc.add(media)

        pagination.append_controls(oc, response, page=page, callback=HandleGenre, id=id, name=name)

        return oc

    return video_service.error_handler.handle_exception(_)

@route('/video/etvnet/new_arrivals')
def GetNewArrivals(page=1, **params):
    def _():
        oc = ObjectContainer(title2=unicode(L('New Arrivals')))

        response = video_service.get_new_arrivals(per_page=common.get_elements_per_page(), page=page)

        for media in HandleMediaList(response['data']['media']):
           oc.add(media)

        pagination.append_controls(oc, response, page=page, callback=GetNewArrivals)

        return oc

    return video_service.error_handler.handle_exception(_)

@route('/video/etvnet/history')
def GetHistory(page=1, **params):
    def _():
        oc = ObjectContainer(title2=unicode(L('History')))

        response = video_service.get_history(per_page=common.get_elements_per_page(), page=page)

        for media in HandleMediaList(response['data']['media']):
           oc.add(media)

        pagination.append_controls(oc, response, page=page, callback=GetHistory)

        return oc

    return video_service.error_handler.handle_exception(_)

def HandleMediaList(response, in_queue=False):
    list = []

    for media in response:
        type = media['type']
        id = media['id']
        name = media['name']
        thumb = media['thumb']

        # if long_name:
        #     on_air = Datetime.ParseDate(media['on_air']).date()
        #     name = unicode(media['name'] + " (" + on_air.strftime("%Y-%m-%d") +")")
        # else:
        #     name = unicode(media['name'])

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

                watch_status=media['watch_status']

                if watch_status == 1:
                    name = "~ " + name
                elif watch_status == 2:
                    name = "* " + name

                list.append(DirectoryObject(key=key, title=name, thumb=thumb))

    return list


@route('/video/etvnet/children')
def HandleChildren(id, name, thumb, in_queue=False, page=1, dir='desc'):
    def _():
        oc = ObjectContainer(title2=unicode(name))

        response = video_service.get_children(int(id), per_page=common.get_elements_per_page(), page=page, dir=dir)

        for media in HandleMediaList(response['data']['children'], in_queue=in_queue):
           oc.add(media)

        bookmarks.append_controls(oc, id=id, name=name, thumb=thumb)
        sorting.append_controls(oc, HandleChildren, id=id, name=name, thumb=thumb, in_queue=in_queue, page=page, dir=dir)

        pagination.append_controls(oc, response, callback=HandleChildren, id=id, name=name, thumb=thumb,
                                   in_queue=in_queue, page=page, dir=dir)

        return oc

    return video_service.error_handler.handle_exception(_)

@route('/video/etvnet/child')
def HandleChild(id, name, thumb, rating_key, description, duration, year, on_air, index, files, container=False):
    oc = ObjectContainer(title2=unicode(name))

    oc.add(MetadataObjectForURL(id, 'movie', name, thumb, rating_key, description, duration, year, on_air, index, files, container))

    if str(container) == 'False':
        bookmarks.append_controls(oc, id=id, name=name, thumb=thumb, rating_key=rating_key,
            description=description, duration=duration, year=year, on_air=on_air, files=files, container=container)

    return oc

def MetadataObjectForURL(id, media_type, name, thumb, rating_key, description, duration, year, on_air, index, files, container):
    if media_type == 'episode':
        video = EpisodeObject(
            rating_key=rating_key,
            show=name,
            summary=unicode(description),
            thumb=thumb,
            # rating=float(1),
            duration=int(duration)*60*1000,
            # year=int(year),
            index=int(index),
            originally_available_at=originally_available_at(on_air)
        )
    elif media_type == 'movie':
        video = MovieObject(
            rating_key=rating_key,
            title=name,
            summary=unicode(description),
            thumb=thumb,
            # rating=float(1),
            duration=int(duration)*60*1000,
            year=int(year),
            # index=index,
            originally_available_at=originally_available_at(on_air)
        )
    else:
        video = VideoClipObject(
            rating_key=rating_key,
            title=name,
            summary=unicode(description),
            thumb=thumb,
            # rating=float(1),
            duration=int(duration)*60*1000,
            year=int(year),
            index=index,
            originally_available_at=originally_available_at(on_air)
        )

    video.key = Callback(HandleChild, id=id, name=name, thumb=thumb,
                         rating_key=rating_key, description=description, duration=duration, year=year,
                         on_air=on_air, index=index, files=files, container=True)

    files = json.loads(urllib.unquote_plus(files))

    video.items = []

    for format, bitrates in video_service.bitrates(files, common.get_format(), common.get_quality_level()).iteritems():
        video.items.extend(MediaObjectsForURL(id=id, format=str(format), bitrates=json.dumps(bitrates)))

    return video

def MediaObjectsForURL(id, format, bitrates):
    media_objects = []

    #resolution = ['720', '360', '360', '360']

    for bitrate in sorted(json.loads(bitrates), reverse=True):
        media_object = MediaObject(
            # # video_resolution=resolution,
            # #
            # # container=Container.MP4,
            # # video_codec=VideoCodec.H264,
            bitrate=bitrate,
            # audio_codec=AudioCodec.AAC,
            # audio_channels=2,
            optimized_for_streaming=True
        )

        part_object = PartObject(key=Callback(PlayIndirectVideo, id=id, format=format, bitrate=str(bitrate)))

        media_object.parts.append(part_object)

        media_objects.append(media_object)

    return media_objects

@indirect
@route('/video/etvnet/play_indirect_video')
def PlayIndirectVideo(id, bitrate, format, **params):
    response = video_service.get_url(id, bitrate=bitrate, format=format, other_server=common.other_server())

    # Log(response['url'])

    if not response['url']:
        common.no_contents()
    else:
        return IndirectResponse(MovieObject, key=RTMPVideoURL(response['url']))

@route('/video/etvnet/play_direct_video')
def PlayDirectVideo(id, bitrate, format, **params):
    response = video_service.get_url(id, bitrate=bitrate, format=format, other_server=common.other_server())

    # Log(response['url'])

    if not response['url']:
        common.no_contents()
    else:
        return Redirect(RTMPVideoURL(response['url']))

def originally_available_at(on_air):
    return Datetime.ParseDate(on_air.replace('+', ' ')).date()
