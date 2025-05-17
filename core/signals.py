from . import models, consumers, enums, dataApis
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

@receiver(post_save, sender=models.Player, dispatch_uid="player")
def player(sender, instance, created, **kwargs):
    if created:
        # Player was created, do something here if needed
        pass
    else:
        # Player was updated, do something here if needed
        data = dataApis.player(instance)
        print(f"Player updated: {data}")
        # Send the updated player data to all websocket consumers
        consumers.wsSendToAll(enums.EventType.SubscriptionUpdateProfile, data)

@receiver(post_save, sender=models.PlayerPresence, dispatch_uid="player_presence")
def player_presence(sender, instance, created, **kwargs):
    if created:
        # PlayerPresence was created, do something here if needed
        pass
    else:
        data = {
            "PlayerId": instance.Player.id,
            "IsOnline": instance.IsOnline,
            "GameSessionId": instance.GameSessionId,
            "AppVersion": instance.AppVersion,
            "Activity": instance.Activity,
            "Private": instance.Private,
            "AvailableSpace": instance.AvailableSpace,
            "GameInProgress": instance.GameInProgress,
        }
        print(f"Player presence updated: {data}")
        # Send the updated player presence data to all websocket consumers
        consumers.wsSendToAll(enums.EventType.SubscriptionUpdatePresence, data)

@receiver(post_save, sender=models.message, dispatch_uid="message")
def message(sender, instance, created, **kwargs):
    if created:
        # Message was created, do something here if needed
        data = {
            "Id": instance.id,
            "FromPlayerId": instance.Sender.id,
            "SentTime": instance.SentTime.isoformat(),
            "Type": instance.Type,
            "Data": instance.Data
        }
        print(f"Message created: {data}")
        # Send the message to the receiver's websocket consumer
        playerWs = consumers.findWsByPlayerId(instance.Receiver.id)
        if playerWs is not None:
            consumers.WsSend(playerWs["consumer"], enums.EventType.MessageReceived, data)
        else:
            print("No websocket found")
    else:
        # Message was updated, do something here if needed
        pass

@receiver(post_save, sender=models.Ban, dispatch_uid="ban")
def ban(sender, instance, created, **kwargs):
    if created:
        playerWs = consumers.findWsByPlayerId(instance.Player.id)
        if playerWs is not None:
            consumers.WsSend(playerWs["consumer"], enums.EventType.ModerationQuitGame, {})
    else:
        # Ban was updated, do something here if needed
        pass

@receiver(post_save, sender=models.Relationship, dispatch_uid="relationship")
def relationship(sender, instance, created, **kwargs):
    if created:
        playerWs = consumers.findWsByPlayerId(instance.Player1.id)
        if playerWs is not None:
            consumers.WsSend(playerWs["consumer"], enums.EventType.RelationshipChanged, dataApis.Relationship(instance))
    else:
        playerWs = consumers.findWsByPlayerId(instance.Player1.id)
        if playerWs is not None:
            consumers.WsSend(playerWs["consumer"], enums.EventType.RelationshipChanged, dataApis.Relationship(instance))