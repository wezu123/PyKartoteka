import json
from os import path

# with open("config.json", "r") as read_json:
#     test = json.load(read_json)
#     print(test)
class Config:
    config_file = "config.json"
    def read_config(self):
        if(path.isfile(self.config_file)):
            with open(self.config_file, "r") as read_json:
                test = json.load(read_json)
                print(test)
        else:
            print(f'Could not find a config file with path "{self.config_file}"!')

config = Config()
config.read_config()