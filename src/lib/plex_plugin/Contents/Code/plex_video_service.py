from etvnet_service import EtvnetService
from plex_config import PlexConfig

class PlexVideoService(EtvnetService):
     def __init__(self):
        config_name = Core.storage.abs_path(Core.storage.join_path(Core.bundle_path, 'Contents', 'etvnet.config'))
        config = PlexConfig(config_name)

        EtvnetService.__init__(self, config)
