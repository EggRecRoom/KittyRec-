def GPKJJKCHILI(FNNIIBJCBOO: str):
    if not FNNIIBJCBOO:
        return None
    array = FNNIIBJCBOO.split(',')
    if array is None or len(array) != 4:
        return None
    for i in range(len(array)):
        if array[i] == "":
            array[i] = None
    return array

def outfitItem(outfitItem: str, colorSwatch, mask, decal):
    if colorSwatch is None:
        colorSwatch = ""
    if mask is None:
        mask = ""
    if decal is None:
        decal = ""
    return f"{outfitItem},{colorSwatch},{mask},{decal}"
import json
from . import models

with open("avs.json") as f:
    data = json.load(f)

def run():
    for x in data:
        guid = GPKJJKCHILI(x["guid"])
        print(guid)
        models.OutfitItem.objects.create(
            friendlyName = x["name"],
            prefab = guid[0],
            colorSwatch = guid[1],
            mask = guid[2],
            decal = guid[3]
        )

    print("done")