import json


def parse_json(path):
    # open json
    with open(path) as f:
        list = json.load(f)
        # for debug
        # print(type(list[0]))
        return list



