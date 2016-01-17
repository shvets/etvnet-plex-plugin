import json

class MediaInfo(dict):
    def __init__(self, type, id, name, thumb, rating_key=None, description=None,
                 duration=None, year=None, on_air=None, files=None):
        super(MediaInfo, self).__init__()

        self['type'] = type
        self['id'] = id
        self['name'] = name
        self['thumb'] = thumb
        self['rating'] = rating_key
        self['description'] = description
        self['duration'] = duration
        self['year'] = year
        self['on_air'] = on_air

        if files:
            self['files'] = json.loads(files)