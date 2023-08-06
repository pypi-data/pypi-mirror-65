from acnh.tools import _search_data, _all_items
from acnh.errors import GameError

items = []


def _process(raw):
    nh = raw['games'].get('nh', {})
    return Item(raw['id'], raw['name'], raw['category'], nh.get('sellPrice', None), nh.get('buyPrices', None),
                nh.get('recipe', None))


def _all():
    all_items = []
    for item in _all_items():
        try:
            all_items.append(_process(item))
        except GameError:
            pass
    return all_items


def get(item_name):
    """
    Get an item from the main item list
    :param item_name: The name of the item you wish to retrieve
    :return: the item object
    """
    item_name = item_name.lower()
    item_name = item_name.replace(" ", "-")
    for item in items:
        if item.id == item_name:
            return item
    raise GameError("{} is not present in New Horizons".format(item_name))


def _search(item_name):
    raw = _search_data(item_name)
    return _process(raw)


def _recipe(recipe: dict):
    recipe_sorted = {}
    for key, value in recipe.items():
        recipe_sorted[key] = {
            'quantity': value,
            'item': _search(key)
        }
    return recipe_sorted


class Item:
    def __init__(self, id, name, category, sell_price, buy_price, recipe):
        self.id = id
        self.name = name
        self.category = category
        self.sell_price = sell_price
        self.buy_price = buy_price
        if recipe is None:
            self.recipe = None
        else:
            self.recipe = _recipe(recipe)

    def __str__(self):
        return self.name

    def to_dict(self):
        normalised_recipe = self.recipe
        if normalised_recipe is not None:
            for key, value in normalised_recipe.items():
                normalised_recipe[key]['item'] = value['item'].to_dict()
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'pricing': {
                'sellPrice': self.sell_price,
                'buyPrice': self.buy_price
            },
            'recipe': normalised_recipe
        }


items = _all()
