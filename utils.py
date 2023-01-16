import json
import os

def pp(data):
    json.dumps(data, indent=4)

def array_from_file(path):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    else:
        return []
