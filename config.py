import json

class ConfigReader:
    def __init__(self, path):
        with open(path) as config_file:
            self.config = json.load(config_file)

    def get_config(self):
        return self.config
