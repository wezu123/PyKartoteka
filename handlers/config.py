import json
from os import path
import logging as log

class Config:
    def __init__(self):        
        self.logger = log.getLogger(__name__)
        self.config_path = "config.json"
        self.running_config = self.read_config()
        self.unsaved_changes = False

    def read_config(self):
        self.logger.info(f'Config path set to {self.config_path}, attempting to open file.')
        if(path.isfile(self.config_path)):
            with open(self.config_path, "r") as read_json:
                conf = json.load(read_json)
                # print(conf)
                return conf
        else:
            self.logger.warning(f'Could not find a config file with path "{self.config_path}"!')
            return False
        
    def save_config(self):
        pass #TODO

    def get_val(self, key):
        try:
            return self.running_config[key]
        except KeyError:
            self.logger.critical(f"Can't find key {key} in running config! Shutting down...")
            exit()

    def set_val(self, key, val):
        try:
            self.running_config[key] = val
            return True
        except KeyError:
            self.logger.error(f'Could not find key "{key}". No changes have been made!')
            return False

# config = Config()
# config.read_config()