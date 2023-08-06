from acnh.tools import _load_data, _all_villagers
from acnh.errors import GameError
import acnh.items

villagers = []


def _all():
    villagers = []
    for villager in _all_villagers():
        try:
            villagers.append(_load(villager))
        except GameError:
            pass
    return villagers


def _load(villager_name):
    """"""
    raw = _load_data("villagers/{}".format(villager_name))
    return Villager(raw["id"], raw["name"], raw["species"], raw["birthday"],
                    raw["games"].get("nh", {}).get("personality", None),
                    raw["games"].get("nh", {}).get("phrase", None),
                    raw["games"].get('nh', {}).get("song", None))


def get(villager_name):
    """
    Get a villager from the main villager list.
    :param villager_name: The name of the villager you wish to retrieve
    :return: the villager object
    """
    villager_name = villager_name.lower()
    villager_name = villager_name.replace(" ", "-")
    for villager in villagers:
        if villager.id == villager_name:
            return villager
    raise GameError("{} is not present in New Horizons".format(villager_name))


class Villager:
    def __init__(self, id, name, species, birthday, personality, phrase, song: str):
        self.id = id
        self.name = name
        self.species = species
        self.birthday = birthday
        self.personality = personality
        self.phrase = phrase
        if song is not None:
            song = song.replace(".", "")
            song = song.replace(" ", "-")
            song = song.lower()
            self.song = acnh.items.get(song)
        else:
            self.song = None

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'species': self.species,
            'birthday': self.birthday,
            'personality': self.personality,
            'phrase': self.phrase,
            'song': self.song.to_dict()
        }


villagers = _all()
