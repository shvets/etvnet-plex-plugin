import json
import os

class Config:
    def __init__(self, config_name):
        self.config_name = config_name
        self.config = {}

    def get_value(self, name):
        if name in self.config.keys():
            return self.config[name]
        else:
            return None

    def load(self):
        self.config.clear()

        if os.path.isfile(self.config_name):
            with open(self.config_name, 'r') as file:
                self.config = json.load(file)

    def save(self, config=None):
        if config:
            self.config = config

        with open(self.config_name, 'w') as file:
            json.dump(self.config, file, indent=4)