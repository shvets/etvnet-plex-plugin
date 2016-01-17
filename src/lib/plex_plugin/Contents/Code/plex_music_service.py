from error_handler import ErrorHandler
from music_service import MusicService
from plex_storage import PlexStorage

class PlexMusicService(MusicService):
     def __init__(self, error_callback=None):
        self.error_handler = ErrorHandler(error_callback)

        storage_name = Core.storage.abs_path(Core.storage.join_path(Core.bundle_path, 'Contents', 'music.storage'))
        self.music_queue = PlexStorage(storage_name)