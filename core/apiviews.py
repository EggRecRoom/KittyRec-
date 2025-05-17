from django.shortcuts import render, HttpResponse
from django.conf import settings as confsettings
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpRequest, HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponseServerError, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from . import models, enums, dataApis, consumers
import uuid
import json
import random
from functools import wraps
import jwt
import sys
import requests
import datetime
from dotenv import load_dotenv
import os
from colorama import Fore
import colorama
import re

colorama.init(autoreset=True)

JWT_SECRET = "Femboys"

hasEmail = True


def NeedToken(requiredScopes=[], requiredRoles=[]):
    def decorator(func):
        @wraps(func)
        def decorated(request, *args, **kwargs):
            bearerToken = request.headers.get("Authorization")
            if not bearerToken:
                return dataApis.abort(401)

            if not bearerToken.startswith("Bearer "):
                return dataApis.abort(401)

            token = bearerToken.split("Bearer ")[1]
            try:
                tokenData = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
                playerId = int(tokenData["sub"])
                token_scopes = tokenData.get("scope", [])
                if not all(scope in token_scopes for scope in requiredScopes):
                    return dataApis.abort(403)
                token_role = tokenData.get("role", [])
                if not all(role in token_role for role in requiredRoles):
                    return dataApis.abort(403)
            except jwt.ExpiredSignatureError:
                print("1")
                return dataApis.abort(401)
            except jwt.InvalidTokenError:
                print("2")
                return dataApis.abort(401)
            except KeyError:
                print("3")
                return dataApis.abort(401)
            except Exception as e:
                print(f"Token decoding error: {e}")
                return dataApis.abort(401)

            return func(request, *args, **kwargs, playerId=playerId)

        return decorated
    return decorator

def getenum(nameOrId, enum) -> (enums.Enum | None):
    """Converts a name or ID to an enum value.
    
    Args:
        nameOrId (str or int): The name or ID to convert.
        enum (enum): The enum class to convert to.
    
    Returns:
        enum: The corresponding enum value, or None if not found.
    """
    try:
        return enum(int(nameOrId))
    except:
        try:
            return enum[nameOrId]
        except:
            return None


from dateutil.parser import parse
def getCurrentTime():
  now = datetime.datetime.now()
  currentTime = now.isoformat()
  return currentTime
def getEndAtTime(EndAt: str):
  StartedAt = getCurrentTime()
  StartedAtSex = parse(StartedAt)
  EndAt = parse(EndAt)
  StartedAtSex = StartedAtSex.timestamp()
  EndAt = EndAt.timestamp()
  Duration = EndAt - StartedAtSex
  return int(Duration)

# Create your views here.

def test(request: HttpRequest):
    if request.method != 'GET':
        return dataApis.abort(405)
    return JsonResponse({"test": "test"})

def versioncheck(request: HttpRequest):
    if request.method != 'GET':
        return dataApis.abort(405)
    return JsonResponse({"ValidVersion": True})

def config(request: HttpRequest):
    if request.method != 'GET':
        return dataApis.abort(405)
    data = {
        "MessageOfTheDay": "Welcome to RecRoom!",
        "CdnBaseUri": "https://cdn-dev.oldrecroom.com",
        "MatchmakingParams": {
            "PreferFullRoomsFrequency": 1.0,
            "PreferEmptyRoomsFrequency": 0.0
        },
        "LevelProgressionMaps": [],
        "DailyObjectives": [],
        "ConfigTable": [],
        "PhotonConfig": {
            "CloudRegion": "jp",
            "CrcCheckEnabled": False,
            "EnableServerTracingAfterDisconnect": False
        }
    }
    return JsonResponse(data, safe=False)

def HowToVideoConfig(request: HttpRequest):
    if request.method != 'GET':
        return dataApis.abort(405)
    video = random.choice(models.HowToVideo.objects.all())
    PlayButton = video.PlayButtonImage
    if PlayButton is None:
        PlayButtonName = ""
    else:
        PlayButtonName = PlayButton.name
    data = {
        "BlobName": video.Video.name.replace("video/", ""),
        "PlayButton": PlayButtonName,
        "Volume": video.Volume,
        "PitchVariation": video.PitchVariation,
        "PitchShift": video.PitchShift,
    }
    return JsonResponse(data, safe=False)

def raido(request: HttpRequest):
    if request.method != 'GET':
        return dataApis.abort(405)
    audios = []
    for x in models.Radio.objects.all():
        audios.append({
            "BlobName": x.audio.name.replace("audio/", ""),
        })

    
    return JsonResponse({"tracks": audios}, safe=False)

@csrf_exempt
def platformlogins(request: HttpRequest):
    if request.method != 'POST':
        return dataApis.abort(405)
    Platform = getenum(request.POST.get("Platform"), enums.PlatformType)
    PlatformId = request.POST.get("PlatformId")
    if Platform is None:
        return dataApis.abort(400)
    if PlatformId is None:
        return dataApis.abort(400)
    if Platform != enums.PlatformType.STEAM:
        return dataApis.abort(400)
    players = []
    for x in models.Login.objects.all():
        if x.Platform == Platform.value and x.PlatformId == PlatformId:
            players.append(dataApis.player(x.Player))
    return JsonResponse(players, safe=False)


@csrf_exempt
def platformlogin(request: HttpRequest):
    if request.method != 'POST':
        return dataApis.abort(405)
    print(request.POST)
    Platform = getenum(request.POST.get("Platform"), enums.PlatformType)
    PlatformId = request.POST.get("PlatformId")
    if Platform is None:
        return dataApis.abort(400)
    if PlatformId is None:
        return dataApis.abort(400)
    if Platform != enums.PlatformType.STEAM:
        return dataApis.abort(400)
    Name = request.POST["Name"]
    AppVersion = request.POST["AppVersion"]
    ClientTimestamp = request.POST["ClientTimestamp"]
    DeviceId = request.POST["DeviceId"]
    PlayerId = request.POST.get("PlayerId")
    BuildTimestamp = request.POST["BuildTimestamp"]
    try:
        AuthParams = json.loads(request.POST["AuthParams"])
    except:
        return dataApis.abort(400)
    
    SteamTicket = AuthParams.get("Ticket")
    Verify = request.POST["Verify"]
    steamREQ = requests.get(f"{confsettings.STEAM_API_URL}ISteamUserAuth/AuthenticateUserTicket/v1?key={confsettings.STEAM_KEY}&appid={confsettings.STEAM_APPID}&ticket={SteamTicket}")
    if steamREQ.status_code != 200:
        return JsonResponse({"PlayerId": 0, "Token": "", "Error": "An unexpected error occurred while communicating with the Steam API."}, safe=False)
    try:
        steamApiJson = steamREQ.json()["response"]
    except:
        return JsonResponse({"PlayerId": 0, "Token": "", "Error": "An unexpected error occurred while processing the Steam API response."}, safe=False)
    print(steamApiJson)
    if steamApiJson.get("error") is not None:
        errorDescription = steamApiJson["error"].get("errordesc", "No error description provided by Steam API.")
        return JsonResponse({"PlayerId": 0, "Token": "", "Error": errorDescription}, safe=False)
    steamParam = steamApiJson.get("params")
    if steamParam is None:
        return JsonResponse({"PlayerId": 0, "Token": "", "Error": "Steam authentication failed. Please try again."}, safe=False)
    if steamParam["vacbanned"]:
        return JsonResponse({"PlayerId": 0, "Token": "", "Error": "Your account appears to be VAC banned and cannot proceed."}, safe=False)
    if PlatformId != steamParam["steamid"]:
        return JsonResponse({"PlayerId": 0, "Token": "", "Error": "Platform ID mismatch."}, safe=False)
    PlatformId = steamParam["steamid"]
    player = None
    if PlayerId is None:
        for x in  models.Login.objects.all():
            if x.Platform == Platform.value:
                if x.PlatformId == PlatformId:
                    return JsonResponse({"PlayerId": 0, "Token": "", "Error": f"This {Platform.name} account is already linked to another user."}, safe=False)
        player = models.Player.objects.create(
            Username=str(uuid.uuid4()),
            DisplayName=Name,
            Email=None
        )
        models.Login.objects.create(
            Platform=Platform.value,
            PlatformId=PlatformId,
            Player=player,
            LastLoginDateTime=datetime.datetime.now()
        )
        models.PlayerPresence.objects.create(
            Player =player,
        )
        models.Avatar.objects.create(
            Player =player,
        )
    else:
        try:
            player = models.Player.objects.get(pk=PlayerId)
        except:
            return dataApis.abort(400)
    time = dataApis.timeshit(datetime.datetime.utcnow())
    jwtD = {
        "iss": "https://auth.rec.net/",
        "client_id": "recnet",
        "role": ["gameClient"],
        "sub": player.id,
        "auth_time": time,
        "idp": "local",
        "iat": time,
        "scope": ["generate"],
        "amr": [
            "cached_login"
        ]
    }
    return JsonResponse({"PlayerId": player.id, "Token": jwt.encode(jwtD, key=JWT_SECRET), "Error": ""}, safe=False)

@NeedToken([], ["gameClient"])
def playerById(request: HttpRequest, playerId, playerId2):
    if request.method != 'GET':
        return dataApis.abort(405)
    print(playerId)
    try:
        player = models.Player.objects.get(pk=playerId2)
    except:
        return dataApis.abort(400)
    return JsonResponse(dataApis.player(player), safe=False)

@NeedToken([], [])
def messages(request: HttpRequest, playerId):
    if request.method != 'GET':
        return dataApis.abort(405)
    messages = []
    for x in models.message.objects.all():
        if x.Receiver.id == playerId:
            Data = x.Data
            if Data is None:
                Data = ""
            messages.append({
                "Id": x.id,
                "FromPlayerId": x.Sender.id,
                "SentTime": x.SentTime,
                "Type": x.Type,
                "Data": Data
            })
    return JsonResponse(messages, safe=False)

@NeedToken([], [])
def relationships(request: HttpRequest, playerId):
    if request.method != 'GET':
        return dataApis.abort(405)
    relationships2 = []
    for x in models.Relationship.objects.all():
        if x.Player1.id == playerId:
            relationships2.append(dataApis.Relationship(x))
    return JsonResponse(relationships2, safe=False)

@NeedToken([], ["gameClient"])
def avatar(request: HttpRequest, playerId):
    if request.method != 'GET':
        return dataApis.abort(405)
    try:
        Avatar = models.Avatar.objects.get(Player_id=playerId)
    except:
        return dataApis.abort(500)
    if Avatar.OutfitSelections is None:
        Avatar.OutfitSelections = ""
    if Avatar.HairColor is None:
        Avatar.HairColor = ""
    if Avatar.SkinColor is None:
        Avatar.SkinColor = ""
    data = {
        "Id": Avatar.id,
        "OutfitSelections": Avatar.OutfitSelections,
        "HairColor": Avatar.HairColor,
        "SkinColor": Avatar.SkinColor
    }

    return JsonResponse(data, safe=False)


@NeedToken([], ["gameClient"])
@csrf_exempt
def avatarset(request: HttpRequest, playerId):
    if request.method != 'POST':
        return dataApis.abort(405)
    jsonData = json.loads(request.body)
    try:
        OutfitSelections = jsonData["OutfitSelections"]
        SkinColor = jsonData["SkinColor"]
        HairColor = jsonData["HairColor"]
    except KeyError as e:
        print(f"Missing required field: {e}")
        return JsonResponse({
            "Error": f"Missing required field: {e}"
        })
    except ValueError as e:
        print(f"Invalid value: {e}")
        return JsonResponse({
            "Error": f"Invalid value"
        })
    try:
        avata = models.Avatar.objects.get(Player_id=playerId)
    except:
        return dataApis.abort(500)
    avata.OutfitSelections = OutfitSelections
    avata.SkinColor = SkinColor
    avata.HairColor = HairColor
    avata.save()
    print(avata)
    return JsonResponse("", safe=False)


@NeedToken([], ["gameClient"])
def settings(request: HttpRequest, playerId):
    if request.method != 'GET':
        return dataApis.abort(405)
    settings = []
    for x in models.Setting.objects.all():
        if x.Player.id == playerId:
            settings.append({
                "Key": x.Key,
                "Value": x.Value
            })
    return JsonResponse(settings, safe=False)

@csrf_exempt
@NeedToken([], ["gameClient"])
def settingsset(request: HttpRequest, action, playerId):
    if request.method != 'POST':
        return dataApis.abort(405)
    jsonData = json.loads(request.body)
    try:
        Key = jsonData["Key"]
        Value = jsonData["Value"]
    except KeyError as e:
        print(f"Missing required field: {e}")
        return JsonResponse({
            "Error": f"Missing required field: {e}"
        })
    except ValueError as e:
        print(f"Invalid value: {e}")
        return JsonResponse({
            "Error": f"Invalid value"
        })
    
    try:
        player = models.Player.objects.get(pk=playerId)
    except:
        return dataApis.abort(500)
    
    if action == "set":
        has = True
        try:
            avata = models.Setting.objects.get(Player_id=playerId, Key=Key)
        except:
            has = False
        if has:
            avata.Value = Value
            avata.save()
        else:
            models.Setting.objects.create(
                Player=player,
                Key=Key,
                Value=Value
            )
    elif action == "remove":
        pass
    else:
        return dataApis.abort(404)
    return JsonResponse("", safe=False)

@NeedToken([], ["gameClient"])
def UnlockedAvatarItems(request: HttpRequest, playerId):
    if request.method != 'GET':
        return dataApis.abort(405)
    unlockedItems = []
    for x in models.MyGiGiftDrop.objects.all():
        if x.Player.id == playerId:
            if x.GiftDrop.OutfitItem is None:
                continue
            unlockedItems.append({
                "Id": x.id,
                "AvatarItemDesc": dataApis.outfitItem(x.GiftDrop.OutfitItem.prefab, x.GiftDrop.OutfitItem.colorSwatch, x.GiftDrop.OutfitItem.mask, x.GiftDrop.OutfitItem.decal),
                "UnlockedLevel": 0
            })

    return JsonResponse(unlockedItems, safe=False)

@NeedToken([], ["gameClient"])
def UnlockedEquipments(request: HttpRequest, playerId):
    if request.method != 'GET':
        return dataApis.abort(405)
    unlockedItems = []
    for x in models.MyGiGiftDrop.objects.all():
        if x.Player.id == playerId:
            if x.GiftDrop.Equipment is None:
                continue
            unlockedItems.append({
                "Id": x.id,
                "PrefabName": x.GiftDrop.Equipment.PrefabName,
                "ModificationGuid": x.GiftDrop.Equipment.ModificationGuid,
                "UnlockedLevel": 0,
            })
    return JsonResponse(unlockedItems, safe=False)

@NeedToken([], ["gameClient"])
def gifts(request: HttpRequest, playerId):
    if request.method != 'GET':
        return dataApis.abort(405)
    gifts = []
    for x in models.Gift.objects.all():
        if x.Player.id == playerId:
            if x.Opened:
                continue
            gifts.append(dataApis.gidt(x))
    return JsonResponse(gifts, safe=False)

def events(request: HttpRequest):
    if request.method != 'GET':
        return dataApis.abort(405)
    eventsD = []
    for x in models.Event.objects.all():
        if x.MaxPlayers == 0:
            x.MaxPlayers = None
        CreatorPlayerId = None
        if x.CreatorPlayer is not None:
            CreatorPlayerId = x.CreatorPlayer.id
        eventsData = {
            "EventId": x.id,
            "Name": x.Name,
            "Description": x.Description,
            "StartTime": x.StartTime,
            "EndTime": x.EndTime,
            "Activity": x.Activity,
            "ActivityLevel": x.ActivityLevel,
            "PosterImageName": x.PosterImage.name,
            "GameSessionId": x.GameSessionId,
            "MaxPlayers": x.MaxPlayers,
            "CreatorPlayerId": CreatorPlayerId,
        }
        eventsD.append(eventsData)
    return JsonResponse(eventsD, safe=False)


@NeedToken([], ["gameClient"])
def charadesWords(request: HttpRequest, playerId):
    if request.method != 'GET':
        return dataApis.abort(405)
    words = []
    return JsonResponse(words, safe=False)

@NeedToken([], ["gameClient"])
@csrf_exempt
def getAllPlayers(request: HttpRequest, playerId):
    if request.method != 'POST':
        return dataApis.abort(405)
    players = []
    jsonData = json.loads(request.body)
    print(jsonData)
    for x in models.Player.objects.all():
        if x.id not in jsonData:
            continue
        players.append(dataApis.player(x))
    return JsonResponse(players, safe=False)


@NeedToken(["generate"], ["gameClient"])
@csrf_exempt
def giftsGenerate(request: HttpRequest, playerId):
    if request.method != 'POST':
        return dataApis.abort(405)
    print(request.POST)
    GiftContext = request.POST.get("GiftContext")
    if GiftContext is None:
        return dataApis.abort(400)
    GiftContext = getenum(GiftContext, enums.Context)
    if GiftContext is None:
        return dataApis.abort(400)
    Message = request.POST.get("Message")
    if Message is None:
        return dataApis.abort(400)
    MyGiftDropIds = []
    for x in models.Gift.objects.all():
        if x.Player.id == playerId:
            MyGiftDropIds.append(x.GiftDrop.id)
    GiftDrops = models.GiftDrop.objects.exclude(id__in=MyGiftDropIds, Context=enums.Context.None_)
    if GiftDrops == []:
        return dataApis.abort(404)
    giftdrope = random.choice(GiftDrops)
    if giftdrope is None:
        return dataApis.abort(404)
    player = models.Player.objects.get(pk=playerId)
    gift = models.Gift.objects.create(
        Player=player,
        GiftDrop=giftdrope,
        Message=Message
    )
    #MyGiGiftDrop = models.MyGiGiftDrop.objects.create(
    #    Player = player,
    #    GiftDrop = giftdrope
    #)
    giftd = dataApis.gidt(gift)
    return JsonResponse(giftd, safe=False)

@NeedToken([], ["gameClient"])
@csrf_exempt
def giftconsume(request: HttpRequest, playerId):
    if request.method != 'POST':
        return dataApis.abort(405)
    Id = request.POST.get("Id")
    if Id is None:
        return dataApis.abort(400)
    UnlockedLevel = request.POST.get("UnlockedLevel")
    if UnlockedLevel is None:
        return dataApis.abort(400)
    giftd = models.Gift.objects.get(pk=Id)
    if giftd.Player.id != playerId:
        return dataApis.abort(403)
    if giftd.Opened:
        return dataApis.abort(400)
    giftd.Opened = True
    giftd.save()
    models.MyGiGiftDrop.objects.create(
        Player=giftd.Player,
        GiftDrop=giftd.GiftDrop
    )
    return JsonResponse("", safe=False)
    


@NeedToken([], ["gameClient"])
@csrf_exempt
def messagessend(request: HttpRequest, playerId):
    if request.method != 'POST':
        return dataApis.abort(405)
    print(request.POST)
    ToPlayerId = int(request.POST["ToPlayerId"])
    Type = getenum(request.POST["Type"], enums.MessageType)
    if Type is None:
        return dataApis.abort(400)
    Dataapi = request.POST["Data"]
    if Dataapi == "":
        Data = None
    else:
        Data = Dataapi
    try:
        Sender = models.Player.objects.get(pk=playerId)
    except:
        return dataApis.abort(500)
    try:
        Receiver = models.Player.objects.get(pk=ToPlayerId)
    except:
        return dataApis.abort(500)
    msg = models.message.objects.create(
        Sender = Sender,
        Receiver = Receiver,
        Type = Type.value,
        Data = Data
    )
    return JsonResponse([], safe=False)


@NeedToken([], ["gameClient"])
@csrf_exempt
def messagesdelete(request: HttpRequest, playerId):
    if request.method != 'POST':
        return dataApis.abort(405)
    Id = request.POST.get("Id")
    if Id is None:
        return dataApis.abort(400)
    try:
        msg = models.message.objects.get(pk=Id)
    except:
        return dataApis.abort(500)
    if msg.Receiver.id != playerId:
        return dataApis.abort(403)
    msg.delete()
    return JsonResponse([], safe=False)


@NeedToken([], ["gameClient"])
@csrf_exempt
def listByPlatformId(request: HttpRequest, playerId):
    if request.method != 'POST':
        return dataApis.abort(405)
    jsonData = json.loads(request.body)
    Platform = getenum(jsonData["Platform"], enums.PlatformType)
    if Platform is None:
        return dataApis.abort(400)
    PlatformIds = jsonData["PlatformIds"]
    if PlatformIds is None:
        return dataApis.abort(400)
    players = []
    for x in models.Login.objects.all():
        if x.Platform == Platform.value and x.PlatformId in PlatformIds:
            players.append({
                "Platform": x.Platform,
                "PlatformId": x.PlatformId,
                "Player": dataApis.player(x.Player)
            })
    print(request.POST)
    return JsonResponse(players, safe=False)

@NeedToken([], ["gameClient"])
def gamesessionsIsFull(request: HttpRequest,gamesessionId, playerId):
    if request.method != 'GET':
        return dataApis.abort(405)
    return JsonResponse({"IsFull": False}, safe=False)

def imgnamedata(request: HttpRequest):
    if request.method != 'GET':
        return dataApis.abort(405)
    img = request.GET.get("img")
    if img is None:
        return dataApis.abort(400)
    try:
        imgdata = models.DynamicPoster.objects.get(Name=img)
    except:
        return dataApis.abort(404)
    return HttpResponse(imgdata.Image.read(), content_type='image/png')


@NeedToken([], ["gameClient"])
@csrf_exempt
def uploadtransient(request: HttpRequest, playerId):
    if request.method != 'POST':
        return dataApis.abort(405)
    gameSessionId = request.GET.get("gameSessionId")
    if gameSessionId is None:
        return dataApis.abort(400)
    image = request.FILES.get("image")
    if image is None:
        return dataApis.abort(400)
    player = models.Player.objects.get(pk=playerId)
    imageD = models.PlayerImage.objects.create(
        Player=player,
        Image=image,
        GameSessionId=gameSessionId
    )
    return JsonResponse({
        "ImageName": imageD.Image.name
    }, safe=False)

def searchPlayer(request: HttpRequest):
    if request.method != 'GET':
        return dataApis.abort(405)
    name = request.GET.get("name")
    if name is None:
        return dataApis.abort(400)
    players = []
    for x in models.Player.objects.all():
        if name.lower() in x.Username.lower() or name.lower() in x.DisplayName.lower():
            players.append(dataApis.player(x))
    return JsonResponse(players, safe=False)

@NeedToken([], ["gameClient"])
@csrf_exempt
def updatePlayerPfp(request: HttpRequest, playerId):
    if request.method != 'POST':
        return dataApis.abort(405)
    image = request.FILES.get("image")
    if image is None:
        return dataApis.abort(400)
    try:
        player = models.Player.objects.get(pk=playerId)
    except:
        return dataApis.abort(500)
    player.ProfileImage = image
    player.save()
    return JsonResponse("", safe=False)

@NeedToken([], ["gameClient"])
@csrf_exempt
def updateDisplayname(request: HttpRequest, playerId):
    if request.method != 'POST':
        return dataApis.abort(405)
    Name = request.POST.get("Name")
    if Name is None:
        return JsonResponse({
            "Success": False,
            "Message": "Name is required."
        }, safe=False)
    try:
        player = models.Player.objects.get(pk=playerId)
    except:
        return JsonResponse({
            "Success": False,
            "Message": "Player not found."
        }, safe=False)
    player.DisplayName = Name
    player.save()
    return JsonResponse({
        "Success": True,
        "Message": "Display name updated successfully."
    }, safe=False)

@NeedToken(["accmake"], ["gameClient"])
@csrf_exempt
def createProfile(request: HttpRequest, playerId):
    if request.method != 'POST':
        return dataApis.abort(405)
    Name = request.POST.get("Name")
    if Name is None:
        return dataApis.abort(400)
    try:
        player = models.Player.objects.get(pk=playerId)
    except:
        return dataApis.abort(500)
    Platform = None
    PlatformId = None
    for x in models.Login.objects.all():
        if x.Player.id == playerId:
            Platform = getenum(x.Platform, enums.PlatformType)
            PlatformId = x.PlatformId
            break
    if Platform is None:
        return dataApis.abort(400)
    if PlatformId is None:
        return dataApis.abort(400)
    newplayer = models.Player.objects.create(
        Username=str(uuid.uuid4()),
        DisplayName=Name,
        Email=None
    )
    models.Login.objects.create(
        Platform=Platform.value,
        PlatformId=PlatformId,
        Player=newplayer,
        LastLoginDateTime=datetime.datetime.now()
    )
    models.PlayerPresence.objects.create(
        Player = newplayer,
    )
    models.Avatar.objects.create(
        Player = newplayer,
    )
    return JsonResponse(dataApis.player(newplayer), safe=False)

@NeedToken([], ["gameClient"])
def blockduration(request: HttpRequest, playerId):
    if request.method != 'GET':
        return dataApis.abort(405)
    try:
        Ban = models.Ban.objects.get(Player_id=playerId)
    except:
        return JsonResponse({"BlockedDuration": 0})
    Duration = getEndAtTime(Ban.EndAt.isoformat())
    if Duration < 0:
        Duration = 0
    return JsonResponse({
        "BlockedDuration": Duration
    }, safe=False)

@NeedToken([], ["gameClient"])
@csrf_exempt
def report(request: HttpRequest, playerId):
    if request.method != 'POST':
        return dataApis.abort(405)
    try:
        player = models.Player.objects.get(pk=playerId)
    except:
        return dataApis.abort(500)
    PlayerIdReported = request.POST.get("PlayerIdReported")
    if PlayerIdReported is None:
        return dataApis.abort(400)
    try:
        PlayerIdReported = int(PlayerIdReported)
        playerReported = models.Player.objects.get(pk=PlayerIdReported)
    except:
        return dataApis.abort(400)
    Reason = getenum(request.POST.get("ReportCategory"), enums.ReportCategory)
    if Reason is None:
        return dataApis.abort(400)
    Activity = request.POST.get("Activity")
    if Activity is None:
        return dataApis.abort(400)
    if player.Developer:
        models.Ban.objects.create(
            Player=playerReported,
            ReportCategory=Reason.value,
            EndAt=datetime.datetime.now() + datetime.timedelta(hours=2),
            Reason = None
        )
    return JsonResponse("", safe=False)

@NeedToken([], ["gameClient"])
@csrf_exempt
def email(request: HttpRequest, playerId):
    if request.method != 'POST':
        return dataApis.abort(405)
    Email = request.POST.get("Email")
    if Email is None:
        return dataApis.abort(400)
    try:
        player = models.Player.objects.get(pk=playerId)
    except:
        return dataApis.abort(500)
    if player.Verified:
        return dataApis.abort(400)
    if player.Email is not None:
        return dataApis.abort(400)
    player.Email = Email
    player.save()
    id = str(uuid.uuid4())
    models.PlayerEmail.objects.create(
        Code = id,
        Player = player,
        Email = Email
    )
    html = render_to_string("ConfirmEmail.html", {"id": id, "baseurl": "email-dev.oldrecroom.com"})
    send_mail("KittyRec - Confirm Your Email", "", confsettings.EMAIL_HOST_USER, [Email], html_message=html)
    return JsonResponse({"Message": ""}, safe=False)

@NeedToken([], ["gameClient"])
def sendfriendrequest(request: HttpRequest, playerId):
    if request.method != 'GET':
        return dataApis.abort(405)
    playerId2 = request.GET["id"]
    if playerId2 is None:
        return dataApis.abort(400)
    try:
        player = models.Player.objects.get(pk=playerId)
    except:
        return dataApis.abort(500)
    try:
        player2 = models.Player.objects.get(pk=playerId2)
    except:
        return dataApis.abort(400)
    try:
        Relationship1 = models.Relationship.objects.get(Player1_id=playerId, Player2_id=playerId2)
    except:
        Relationship1 = models.Relationship.objects.create(
            Player1 = player,
            Player2 = player2,
            RelationshipType = enums.RelationshipType.None_.value
        )
    try:
        Relationship2 = models.Relationship.objects.get(Player1_id=playerId2, Player2_id=playerId)
    except:
        Relationship2 = models.Relationship.objects.create(
            Player1 = player2,
            Player2 = player,
            RelationshipType = enums.RelationshipType.None_.value
        )
    Relationship1.RelationshipType = enums.RelationshipType.FriendRequestSent.value
    Relationship2.RelationshipType = enums.RelationshipType.FriendRequestReceived.value
    Relationship1.save()
    Relationship2.save()
    msg = models.message.objects.create(
        Sender = player,
        Receiver = player2,
        Type = enums.MessageType.FriendInvite.value,
        Data = None
    )
    RelationshipData = dataApis.Relationship(Relationship1)
    return JsonResponse(RelationshipData, safe=False)

@NeedToken([], ["gameClient"])
def acceptfriendrequest(request: HttpRequest, playerId):
    if request.method != 'GET':
        return dataApis.abort(405)
    playerId2 = request.GET["id"]
    if playerId2 is None:
        return dataApis.abort(400)
    try:
        player = models.Player.objects.get(pk=playerId)
    except:
        return dataApis.abort(500)
    try:
        player2 = models.Player.objects.get(pk=playerId2)
    except:
        return dataApis.abort(400)
    try:
        Relationship1 = models.Relationship.objects.get(Player1_id=playerId, Player2_id=playerId2)
    except:
        Relationship1 = models.Relationship.objects.create(
            Player1 = player,
            Player2 = player2,
            RelationshipType = enums.RelationshipType.None_.value
        )
    try:
        Relationship2 = models.Relationship.objects.get(Player1_id=playerId2, Player2_id=playerId)
    except:
        Relationship2 = models.Relationship.objects.create(
            Player1 = player2,
            Player2 = player,
            RelationshipType = enums.RelationshipType.None_.value
        )
    if Relationship2.RelationshipType != enums.RelationshipType.FriendRequestSent:
        return dataApis.abort(403)
    Relationship1.RelationshipType = enums.RelationshipType.Friend.value
    Relationship2.RelationshipType = enums.RelationshipType.Friend.value
    Relationship1.save()
    Relationship2.save()
    msg = models.message.objects.create(
        Sender = player,
        Receiver = player2,
        Type = enums.MessageType.FriendRequestAccepted.value,
        Data = None
    )
    RelationshipData = dataApis.Relationship(Relationship1)
    return JsonResponse(RelationshipData, safe=False)

@NeedToken([], ["gameClient"])
def removefriend(request: HttpRequest, playerId):
    if request.method != 'GET':
        return dataApis.abort(405)
    playerId2 = request.GET["id"]
    if playerId2 is None:
        return dataApis.abort(400)
    try:
        player = models.Player.objects.get(pk=playerId)
    except:
        return dataApis.abort(500)
    try:
        player2 = models.Player.objects.get(pk=playerId2)
    except:
        return dataApis.abort(400)
    try:
        Relationship1 = models.Relationship.objects.get(Player1_id=playerId, Player2_id=playerId2)
    except:
        Relationship1 = models.Relationship.objects.create(
            Player1 = player,
            Player2 = player2,
            RelationshipType = enums.RelationshipType.None_.value
        )
    try:
        Relationship2 = models.Relationship.objects.get(Player1_id=playerId2, Player2_id=playerId)
    except:
        Relationship2 = models.Relationship.objects.create(
            Player1 = player2,
            Player2 = player,
            RelationshipType = enums.RelationshipType.None_.value
        )
    Relationship1.RelationshipType = enums.RelationshipType.None_.value
    Relationship2.RelationshipType = enums.RelationshipType.None_.value
    Relationship1.save()
    Relationship2.save()
    RelationshipData = dataApis.Relationship(Relationship1)
    return JsonResponse(RelationshipData, safe=False)

@NeedToken([], ["gameClient"])
@csrf_exempt
def sendMultiple(request: HttpRequest, playerId):
    if request.method != 'POST':
        return dataApis.abort(405)
    Dataapi = json.loads(request.body)
    ToPlayerIds = Dataapi["ToPlayerIds"]
    Type = getenum(Dataapi["Type"], enums.MessageType)
    if Type is None:
        return dataApis.abort(400)
    Dataapi = Dataapi["Data"]
    if Dataapi == "":
        Data = None
    else:
        Data = Dataapi
    try:
        Sender = models.Player.objects.get(pk=playerId)
    except:
        return dataApis.abort(500)
    players = []
    for x in ToPlayerIds:
        try:
            players.append(models.Player.objects.get(pk=x))
        except:
            pass
    for x in players:
        msg = models.message.objects.create(
            Sender = Sender,
            Receiver = x,
            Type = Type.value,
            Data = Data
        )
    return JsonResponse([], safe=False)

def challenge(request: HttpRequest):
    if request.method != 'GET':
        return dataApis.abort(405)
    challenges = models.ChallengeMap.objects.all()
    print(len(challenges))
    if len(challenges) == 0:
        return JsonResponse({
            "Success": False,
            "Message": ""
        })
    challengeMap = challenges[0]
    Gifts = []
    for x in challengeMap.GiftsDrops.all():
        Gifts.append(dataApis.giftDrop(x))
    Challenges = [
        {
            "ChallengeId": 1,
            "Name": "test 1",
            "Config": "",
            "Description": "just a test 1",
            "Tooltip": "just a test 1",
        },
        {
            "ChallengeId": 2,
            "Name": "test 2",
            "Config": "",
            "Description": "just a test 2",
            "Tooltip": "just a test 2"
        },
        {
            "ChallengeId": 3,
            "Name": "test 3",
            "Config": "",
            "Description": "just a test 3",
            "Tooltip": "just a test 3"
        }
    ]
    challengeJson = {
        "ChallengeMapId": challengeMap.id,
        "StartAt": challengeMap.StartAt.isoformat(),
        "EndAt": challengeMap.EndAt.isoformat(),
        "ServerTime": getCurrentTime(),
        "Challenges": Challenges,
        "Gifts": Gifts
    }
    print(challengeJson)
    challengeData = json.dumps(challengeJson)
    print(challengeData)
    return JsonResponse({
        "Success": True,
        "Message": challengeData
    })
#PUBLIC APIS
def pubPlayerByUsername(request: HttpRequest):
    if request.method != 'GET':
        return dataApis.abort(405)
    username = request.GET.get("username")
    if username is None:
        return dataApis.abort(404)
    try:
        player = models.Player.objects.get(Username__iexact=username)
    except models.Player.DoesNotExist:
        return dataApis.abort(404)
    playerjson = {
        "Id": player.id,
        "Username": player.Username,
        "DisplayName": player.DisplayName,
        "XP": player.XP,
        "Level": player.Level,
        "ProfileImageName": player.ProfileImage.name,
    }
    return JsonResponse(playerjson, safe=False)
def pubPlayerById(request: HttpRequest, playerId):
    if request.method != 'GET':
        return dataApis.abort(405)
    if playerId is None:
        return dataApis.abort(404)
    try:
        player = models.Player.objects.get(pk=playerId)
    except:
        return dataApis.abort(404)
    playerjson = {
        "Id": player.id,
        "Username": player.Username,
        "DisplayName": player.DisplayName,
        "XP": player.XP,
        "Level": player.Level,
        "ProfileImageName": player.ProfileImage.name,
    }
    return JsonResponse(playerjson, safe=False)

@csrf_exempt
def updateUsernamePassword(request: HttpRequest):
    if request.method != 'POST':
        return dataApis.abort(405)
    try:
        code = request.POST["code"]
        username = request.POST["username"]
        password = request.POST["password"]
    except:
        return dataApis.abort(400)
    try:
        emaild = models.PlayerEmail.objects.get(Code=code)
    except:
        return JsonResponse({
            "success": False,
            "error": "No code provided for update."
        })
    if emaild.Used:
        return JsonResponse({
            "success": False,
            "error": "No code provided for update."
        })
    playerfound = False
    try:
        models.Player.objects.get(Username__iexact=username)
        playerfound = True
    except:
        playerfound = False
    if playerfound:
        return JsonResponse({
            "success": False,
            "error": "Username is not available."
        })
    if not re.search("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*]).{8,}$", password):
        return JsonResponse({
            "success": False,
            "error": "Password does not meet the requirements."
        })
    emaild.Used = True
    emaild.save()
    player = emaild.Player
    player.Username = username
    player.Email = emaild.Email
    player.Verified = True
    player.Password = dataApis.hashPassword(password)
    player.save()
    return JsonResponse({
            "success": True
        })
