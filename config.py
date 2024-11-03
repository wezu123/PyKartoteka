import json
from os import path

# with open("config.json", "r") as read_json:
#     test = json.load(read_json)
#     print(test)
class Config:
    def __init__(self):
        self.config_file = "config.json"
        self.running_config = self.read_config()
        self.unsaved_changes = False

    def read_config(self):
        if(path.isfile(self.config_file)):
            with open(self.config_file, "r") as read_json:
                conf = json.load(read_json)
                # print(conf)
                return conf
        else:
            print(f'Could not find a config file with path "{self.config_file}"!')
            return False
        
    def save_config(self):
        pass

    def get_val(self, key):
        try:
            return self.running_config[key]
        except KeyError:
            print(f"Can't find key {key} in running config! Shutting down...")
            exit()

    def set_val(self, key, val):
        try:
            self.running_config[key] = val
            return True
        except KeyError:
            return False

# config = Config()
# config.read_config()