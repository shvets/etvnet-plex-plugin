from etvnet_service import EtvnetService
from error_handler import ErrorHandler
from plex_config import PlexConfig

class PlexVideoService(EtvnetService):
     def __init__(self, error_callback=None):
        self.error_handler = ErrorHandler(error_callback)

        config_name = Core.storage.abs_path(Core.storage.join_path(Core.bundle_path, 'Contents', 'etvnet.config'))
        config = PlexConfig(config_name)

        EtvnetService.__init__(self, config)
