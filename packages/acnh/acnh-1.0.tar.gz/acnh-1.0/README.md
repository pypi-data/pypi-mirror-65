# Animal Crossing: New Horizons Python Dataset

## Installation

`pip install acnh`

## Example code

```python 
import acnh

# Villagers
pip install twine
rosie = acnh.villagers.get('rosie')
print("Rosie's fav song:")
print(rosie.song.name)

print("Total amount of villagers:")
print(len(acnh.villagers.villagers))
# Items


seabass = acnh.items.get('sea bass')
print("How much a sea bass sells for, and it's currency:")
print(seabass.sell_price['currency'])
print(seabass.sell_price['value'])

print("Total amount of items:")
print(len(acnh.items.items))
```

## Scope

### Villagers

You can retrieve the following info about villagers:
- Name
- Species
- Birthday
- Personality
- Phrase
- Song

Please note song is of type `Item` (read below for more info!). This means, for example, the following is valid (albeit ugly) to find how much Pietro's favourite song (K.K Parade) is to buy.

`acnh.villagers.get('pietro').song.pricing.buy_price`

You can use `acnh.villagers.villagers` as a `list` of ALL villagers in New Horizons we have data for.

### Items

Currently, you can retrieve the following data:
- Item Name
- Buy Price (including the currency type for items bought with Nook Miles)
- Sell Price (including the currency type for items bought with Nook Miles)
- Category
- Recipe

Recipes will resolve each sub recipe down to the most basic components. A representation of this is shown in JSON as follows:
```json
"recipe": {
    "flimsy-axe": {
      "quantity": 1,
      "item": {
        "id": "flimsy-axe",
        "name": "Flimsy Axe",
        "category": "Tools",
        "pricing": {
          ...
        },
        "recipe": {
          ...
        }
      }
    },
    "wood": {
      "quantity": 3,
      "item": {
        ...
      }
  }
}

Pricing will be `NoneType` if it does not exist (IE: item cannot be bought / sold), so please check this if using pricing information.

You can use `acnh.items.items` as a `list` of ALL items in New Horizons we have data for.
```
## Thanks / licensing
Many thanks to [VillagerDB](https://github.com/jefflomacy/villagerdb) for the item dataset


Animal Crossing is a registered trademark of Nintendo. This project in no way claims ownership of any intellectual property associated with Animal Crossing. 