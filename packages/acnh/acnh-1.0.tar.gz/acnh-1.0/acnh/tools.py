import json
import pathlib
from os import listdir
from acnh.errors import GameError

path = str(pathlib.Path(__file__).parent.absolute()) + "/raw_data/{fileName}"


def _get_item(item_name):
    return _load_data("items/{}".format(item_name))


def _load_data(data_file):
    try:
        with open(path.format(fileName="{}.json".format(data_file)), 'r') as f:
            a = json.loads(f.read())
            if "nh" not in a['games']:
                raise FileNotFoundError
            return a
    except FileNotFoundError:
        raise GameError("{} is not present in New Horizons".format(data_file))


def _search_data(data_file: str):
    data_file = data_file.lower()
    data_file = data_file.replace(" ", "-")
    for file in pathlib.Path(path.format(fileName='items')).rglob(data_file + ".json"):
        file = str(file)
        file = file.replace(path.format(fileName='items/'), "")
        file = file.replace('.json', "")
        return _get_item(file)
    raise GameError("{} is not present in New Horizons".format(data_file))


def _all_items():
    files = []
    paths = pathlib.Path(path.format(fileName='items')).rglob("*.json")
    paths = list(paths)
    paths.sort()
    for file in paths:
        file = str(file)
        file = file.replace(path.format(fileName='items/'), "")
        file = file.replace('.json', "")
        try:
            files.append(_get_item(file))
        except GameError:
            pass
    return files


def _all_villagers():
    files = (listdir(path.format(fileName="villagers")))
    villagers = []
    for file in files:
        try:
            villagers.append(file.replace(".json", ""))
        except GameError:
            pass
    return villagers
