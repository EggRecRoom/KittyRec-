from . import models
from django.shortcuts import render, HttpResponse
import datetime
import re
import bcrypt

def hashPassword(password: str):
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")

def checkHashPass(rawPassword: str, hashPassword: str):
    return bcrypt.checkpw(rawPassword, hashPassword)


def player(playerData: models.Player) -> dict:
    """Converts player data to a dictionary format.

    Args:
        playerData (models.Player): Player data object.

    Returns:
        dict: Dictionary representation of the player data.
    """
    HasEmail = False
    if playerData.Email is not None:
        HasEmail = True

    return {
        "Id": playerData.id,
        "Username": playerData.Username,
        "DisplayName": playerData.DisplayName,
        "XP": playerData.XP,
        "Level": playerData.Level,
        "Reputation": playerData.Reputation,
        "Verified": playerData.Verified,
        "Developer": playerData.Developer,
        "HasEmail": HasEmail,
        "CanReceiveInvites": False,
        "ProfileImageName": playerData.ProfileImage.name,
    }

def Relationship(Relationship: models.Relationship) -> dict:
    return {
        "Id": Relationship.id,
        "PlayerID": Relationship.Player2.id,
        "RelationshipType": Relationship.RelationshipType,
        "Mute": Relationship.Mute,
        "Ignore": Relationship.Ignore
    }




def abort(status_code: int):
    d = HttpResponse("")
    d.status_code = status_code
    return d

def timeshit(iso):
    time = datetime.datetime.fromisoformat(str(iso))
    unixTimestamp = int(time.timestamp())
    return unixTimestamp

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


def gidt(giftData: models.Gift) -> dict:
    """Converts gift data to a dictionary format.

    Args:
        giftData (models.Gift): Gift data object.

    Returns:
        dict: Dictionary representation of the gift data.
    """
    AvatarItemDesc = ""
    if giftData.GiftDrop.OutfitItem is not None:
        OutfitItem = giftData.GiftDrop.OutfitItem
        AvatarItemDesc = outfitItem(OutfitItem.prefab, OutfitItem.colorSwatch, OutfitItem.mask, OutfitItem.decal)
    EquipmentPrefabName = ""
    ModificationGuid = ""
    if giftData.GiftDrop.Equipment is not None:
        EquipmentPrefabName = giftData.GiftDrop.Equipment.PrefabName
        ModificationGuid = giftData.GiftDrop.Equipment.ModificationGuid
    return {
        "Id": giftData.id,
        "GiftDropId": giftData.GiftDrop.id,
        "AvatarItemDesc": AvatarItemDesc,
        "Xp": giftData.GiftDrop.Xp,
        "GiftContext": giftData.GiftDrop.Context,
        "GiftRarity": giftData.GiftDrop.Rarity,
        "Message": giftData.Message,
        "EquipmentPrefabName": EquipmentPrefabName,
        "EquipmentModificationGuid": ModificationGuid,
    }

def isValidEemail(email):
    """
    Checks if a given string is a valid email address using regular expressions.

    Args:
        email (str): The string to validate.

    Returns:
        bool: True if the string is a valid email, False otherwise.
    """
    regex = r"^[\\w!#$%&'*+\\-/=?\\^_`{|}~]+(\\.[\\w!#$%&'*+\\-/=?\\^_`{|}~]+)*@((([\\-\\w]+\\.)+[a-zA-Z]{2,4})|(([0-9]{1,3}\\.){3}[0-9]{1,3}))$"
    match = re.match(regex, email)
    return bool(match)

def giftDrop(giftDropData: models.GiftDrop) -> dict:
    """Converts GiftDrop data to a dictionary format.

    Args:
        giftDropData (models.Gift): Gift data object.

    Returns:
        dict: Dictionary representation of the gift data.
    """
    AvatarItemDesc = ""
    if giftDropData.OutfitItem is not None:
        OutfitItem = giftDropData.OutfitItem
        AvatarItemDesc = outfitItem(OutfitItem.prefab, OutfitItem.colorSwatch, OutfitItem.mask, OutfitItem.decal)
    EquipmentPrefabName = ""
    ModificationGuid = ""
    if giftDropData.Equipment is not None:
        EquipmentPrefabName = giftDropData.Equipment.PrefabName
        ModificationGuid = giftDropData.Equipment.ModificationGuid
    return {
        "GiftDropId": giftDropData.id,
        "AvatarItemDesc": AvatarItemDesc,
        "Xp": 0,
        "Level": 0,
        "GiftContext": giftDropData.Context,
        "GiftRarity": giftDropData.Rarity,
        "EquipmentPrefabName": EquipmentPrefabName,
        "EquipmentModificationGuid": ModificationGuid
    }