from datetime import date

def get_language():
    return Prefs['language'].split('/')[1]

def other_server():
    return int(Prefs['other_server'] == 'Yes')

def get_time_shift():
    return int(Prefs['time_shift'].split('/')[1])

def get_elements_per_page():
    return int(Prefs['elements_per_page'])

def get_format():
    if Prefs['format'] == 'MP4':
        return 'mp4'
    elif Prefs['format'] == 'WMV':
        return 'wmv'
    elif Prefs['format'] == 'All Formats':
        return None
    else:
       return None

def get_quality_level():
    if Prefs['quality_level'] == 'Best':
        return 4
    elif Prefs['quality_level'] == 'High':
        return 3
    elif Prefs['quality_level'] == 'Medium':
        return 2
    elif Prefs['quality_level'] == 'Low':
        return 1
    elif Prefs['quality_level'] == "All Levels":
        return None
    else:
        return None

def validate_prefs():
    language = get_language()

    if Core.storage.file_exists(Core.storage.abs_path(
        Core.storage.join_path(Core.bundle_path, 'Contents', 'Strings', '%s.json' % language)
    )):
        Locale.DefaultLocale = language
    else:
        Locale.DefaultLocale = 'en-us'

def no_contents(name=None):
    if not name:
        name = 'Error'

    return ObjectContainer(header=unicode(L(name)), message=unicode(L('No entries found')))
