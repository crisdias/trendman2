import json
import os
import pprint

def pp(data):
    pprint.pprint(data)

def array_from_file(path):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    else:
        return []

def load_config():
    import toml

    with open('./data/config.toml', 'r') as f:
        return toml.load(f)