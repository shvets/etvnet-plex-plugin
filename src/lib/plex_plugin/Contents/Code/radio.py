@route('/video/etvnet/radio_menu')
def GetRadioMenu():
    oc = ObjectContainer(title2=unicode(L('Radio')))

    stations = radio_service.get_stations()

    for station in stations:
        id = station['id']
        name = station['name']

        oc.add(DirectoryObject(
            key=Callback(HandleRadio, id=id),
            title=unicode(L(name))
        ))

    return oc

@route('/video/etvnet/radio')
def HandleRadio(id):
    response = radio_service.get_station(id=id)

    title = response['station_title']

    oc = ObjectContainer(title2=unicode(L(title)))

    track_title = response['track_title']

    bitrates = {"m4a": [64], 'mp3': [128]}

    format = 'mp3'

    url = response['player_data'][format]

    oc.add(GetTrack(id='id', title=title, track_title=track_title, format=format, bitrates=bitrates[format], url=url))

    return oc

@route('/video/etvnet/track')
def GetTrack(id, title, track_title, format, bitrates, url, container=False):
    track = MetadataObjectForURL(id, title, track_title, format, bitrates, url, container)

    if container:
        return ObjectContainer(objects = [track])
    else:
        return track

def MetadataObjectForURL(id, title, track_title, format, bitrates, url, container):
    track = TrackObject(
        # url=url,
        key=Callback(GetTrack, id=id, title=title, track_title=track_title, format=format, bitrates=bitrates, url=url, container=True),
        rating_key = 'rating_key',
        title = title,
        # summary=unicode(description),
        # album = 'album',
        artist = track_title
        # thumb = 'thumb'
    )

    track.items = MediaObjectsForURL(format, bitrates, url)

    return track

def MediaObjectsForURL(format, bitrates, url):
    if 'm4a' in format:
        container = Container.MP4
        audio_codec = AudioCodec.AAC
    else:
        container = Container.MP3
        audio_codec = AudioCodec.MP3

    media_objects = []

    for bitrate in sorted(bitrates, reverse=True):
        media_object = MediaObject(
            container = container,
            optimized_for_streaming=True
        )

        part_object = PartObject(key=Callback(PlayRadio, url=url))

        audio_stream = AudioStreamObject(
            codec = audio_codec,
            channels = 2,
            bitrate=str(bitrate)
        )

        part_object.streams = [audio_stream]

        media_object.parts.append(part_object)

        media_objects.append(media_object)

    return media_objects

@route('/video/etvnet/play_audio')
def PlayRadio(url):
    return Redirect(url)
