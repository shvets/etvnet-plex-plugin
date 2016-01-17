import json
import time
from config import Config

class PlexConfig(Config):
    def load(self):
        self.config.clear()

        if Core.storage.file_exists(self.config_name):
            self.config = json.loads(str(Core.storage.load(self.config_name)))

    def save(self, config=None):
        if config:
            for key, val in config.items():
                self.config[key] = val

        if 'expires_in' in self.config:
            self.config['expires'] = int(time.time()) + int(self.config['expires_in'])

        Core.storage.save(self.config_name, json.dumps(self.config, indent=4))
