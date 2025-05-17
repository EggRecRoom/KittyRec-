from django.urls import path
from . import apiviews

#!This Is Old API URLS!

urlpatterns = [
    #!path('versioncheck/v3', apiviews.versioncheck),
    #!path('config/v2', apiviews.config),
    #!path('howToVideo/v2/random', apiviews.HowToVideoConfig),
    #!path('platformlogin/v1/profiles', apiviews.platformlogins),
    #!path('platformlogin/v5', apiviews.platformlogin),
    #!path('players/v1/<int:playerId2>', apiviews.playerById),
    #!path('messages/v2/get', apiviews.messages),
    #!path('relationships/v2/get', apiviews.relationships),
    #!path('avatar/v2', apiviews.avatar),
    #!path('avatar/v2/set', apiviews.avatarset),
    #!path('settings/v2/', apiviews.settings),
    #!path('settings/v2/<action>', apiviews.settingsset),
    #!path('avatar/v3/items', apiviews.UnlockedAvatarItems),
    #!path('equipment/v1/getUnlocked', apiviews.UnlockedEquipments),
    #!path('avatar/v2/gifts', apiviews.gifts),
    #!path('events/v2/list', apiviews.events),
    #!path('activities/charades/v1/words', apiviews.charadesWords),
    #!path('players/v1/list', apiviews.getAllPlayers),
    #!path('avatar/v2/gifts/generate', apiviews.giftsGenerate),
    #!path('messages/v2/send', apiviews.messagessend),
    #!path('messages/v2/delete', apiviews.messagesdelete),
    #!path('players/v1/listByPlatformId', apiviews.listByPlatformId),
    #!path('images/v1/named', apiviews.imgnamedata),
    #!path('gamesessions/v1/isfull/<gamesessionId>', apiviews.gamesessionsIsFull),
    #!path('images/v1/uploadtransient', apiviews.uploadtransient),
]