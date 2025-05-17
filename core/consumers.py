import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from . import models, enums
import uuid
import json
from colorama import Fore
from RecNet import discord

Notifications = []


def WsSend(ws: WebsocketConsumer, Id: enums.EventType, Msg):
    """"Send a message to the websocket consumer.
    Args:
        ws (WebsocketConsumer): The websocket consumer to send the message to.
        Id (enums.EventType): The ID of the message.
        Msg: The message to send.
    """
    jsonData = {
        "Id": Id.value,
        "Msg": Msg
    }
    data = {
            "SessionId": 69
        }
    data.update(jsonData)
    print(f"{Fore.LIGHTMAGENTA_EX}Websocket sent \"{data}\" to {ws}")
    ws.send(json.dumps(data))


def wsSendToAll(Id, Msg: enums.EventType):
    """Send a message to all websocket consumers.
    Args:
        Id (enums.EventType): The ID of the message.
        Msg: The message to send.
    """
    for x in Notifications:
        WsSend(x["consumer"], Id, Msg)

def findWsByPlayerId(playerId: int):
    for x in Notifications:
        if x["playerId"] is playerId:
            return x
    return

class NotificationConsumer(WebsocketConsumer):
    global Notifications
    def connect(self):
        Notifications.append({
            "uuid": str(uuid.uuid4()),
            "playerId": None,
            "consumer": self,
        })
        print(self)
        self.accept()
        data = {
            "SessionId": 1
        }
        WsSend(self, enums.EventType.SubscriptionListUpdated, {"PlayerIds": []})
    
    def receive(self: WebsocketConsumer, text_data):
        text_data_json = dict(json.loads(text_data))
        consumer = None
        for x in Notifications:
            if x["consumer"] == self:
                consumer = x
                if x["playerId"] is None:
                    x.update({
                        "playerId": int(text_data_json["PlayerId"])
                    })
        if consumer is None:
            self.close(1, "wtf")
        ff = text_data_json
        api = ff.get("api")
        param = ff.get("param")
        if api is not None:
            print(f"{Fore.LIGHTMAGENTA_EX}Websocket api got \"{api}\"")
            print(f"{Fore.LIGHTMAGENTA_EX}Websocket api received \"{param}\"")
            if api == "presence/v1":
                playerPresence = models.PlayerPresence.objects.get(Player_id=consumer["playerId"])
                playerPresence.IsOnline = True
                playerPresence.GameSessionId = param["GameSessionId"]
                playerPresence.AppVersion = param["AppVersion"]
                oldActivity = playerPresence.Activity
                playerPresence.Activity = param["Activity"]
                playerPresence.Private = param["Private"]
                playerPresence.AvailableSpace = param["AvailableSpace"]
                playerPresence.GameInProgress = param["GameInProgress"]
                playerPresence.save()
                if playerPresence.Activity is not None:
                    if oldActivity != playerPresence.Activity:
                        title = f"{playerPresence.Player.DisplayName} is heading over to {playerPresence.Activity}!"
                        paylo = {
                          "title": f"{playerPresence.Player.DisplayName} is heading over to {playerPresence.Activity}!",
                          "color": 7209178
                        }
                        discord.sendEmbed(paylo, 1358573746528714852)
        #WsSend(self, {})

    def disconnect(self: WebsocketConsumer, close_code):
        print(close_code)
        for x in Notifications:
            if x["consumer"] == self:
                if x["playerId"] is not None:
                    playerPresence = models.PlayerPresence.objects.get(Player_id=x["playerId"])
                    playerPresence.IsOnline = False
                    playerPresence.GameSessionId = None
                    playerPresence.Activity = None
                    playerPresence.Private = False
                    playerPresence.AvailableSpace = 0
                    playerPresence.GameInProgress = False
                    playerPresence.save()
                    paylo = {
                        "title": f"{playerPresence.Player.DisplayName} is now offline.",
                        "color": 7209178
                    }
                    discord.sendEmbed(paylo, 1358573746528714852)
                    Notifications.remove(x)
                else:
                    Notifications.remove(x)
                print(Notifications)