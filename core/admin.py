from django.contrib import admin

# Register your models here.

from . import models

class PlayerAdmin(admin.ModelAdmin):
    list_display = ("Username", "DisplayName", "Verified", "Developer")
    search_fields = ("Username", "DisplayName")
    list_filter = ("Verified", "Developer")
    list_per_page = 20
admin.site.register(models.Player, PlayerAdmin)

class EquipmentAdmin(admin.ModelAdmin):
    list_display = ("FriendlyName", "PrefabName", "ModificationGuid")
    search_fields = ("FriendlyName", "PrefabName", "ModificationGuid")
    list_filter = ("PrefabName",)
    list_per_page = 20
admin.site.register(models.Equipment, EquipmentAdmin)

class LoginAdmin(admin.ModelAdmin):
    list_display = ("Player", "Platform", "PlatformId")
    search_fields = ("Player__Username", "PlatformId")
    list_filter = ("Platform",)
    list_per_page = 20
admin.site.register(models.Login, LoginAdmin)

class PlayerPresenceAdmin(admin.ModelAdmin):
    list_display = ("Player", "IsOnline", "Private", "GameInProgress")
    search_fields = ("Player__Username",)
    list_filter = ("IsOnline", "Private", "GameInProgress", "GameSessionId")
    list_per_page = 20
admin.site.register(models.PlayerPresence, PlayerPresenceAdmin)

class messageAdmin(admin.ModelAdmin):
    list_display = ("id", "Sender", "Receiver", "Type")
    search_fields = ("Sender__Username", "Receiver__Username")
    list_filter = ("Type",)
    list_per_page = 20
admin.site.register(models.message, messageAdmin)

class AvatarAdmin(admin.ModelAdmin):
    list_display = ("Player",)
    search_fields = ("Player__Username",)
    list_per_page = 20
admin.site.register(models.Avatar, AvatarAdmin)

class SettingAdmin(admin.ModelAdmin):
    list_display = ("Player", "Key", "Value")
    search_fields = ("Player__Username",)
    list_filter = ("Key",)
    list_per_page = 20
admin.site.register(models.Setting, SettingAdmin)

class EventAdmin(admin.ModelAdmin):

    list_display = ("Name", "StartTime", "EndTime", "Activity", "ActivityLevel")
    search_fields = ("Name",)
    list_filter = ("Activity", "ActivityLevel")
    list_per_page = 20
admin.site.register(models.Event, EventAdmin)

class DynamicPosterAdmin(admin.ModelAdmin):
    list_display = ("Name",)
    search_fields = ("Name",)
    list_filter = ()
    list_per_page = 20
admin.site.register(models.DynamicPoster, DynamicPosterAdmin)

class PlayerImageAdmin(admin.ModelAdmin):
    list_display = ("Player", "Image", "GameSessionId")
    search_fields = ("Player__Username", "GameSessionId")
    list_per_page = 20
admin.site.register(models.PlayerImage, PlayerImageAdmin)

class HowToVideoAdmin(admin.ModelAdmin):
    list_display = ("Video", "PlayButtonImage", "Volume")
    search_fields = ("Video",)
    list_filter = ()
    list_per_page = 20
admin.site.register(models.HowToVideo, HowToVideoAdmin)

class RadionAdmin(admin.ModelAdmin):
    list_display = ("audio", "AudioType")
    search_fields = ("audio",)
    list_filter = ("AudioType",)
    list_per_page = 20
admin.site.register(models.Radio, RadionAdmin)

class OutfitItemAdmin(admin.ModelAdmin):
    list_display = ("friendlyName",)
    search_fields = ("friendlyName",)
    list_filter = ("prefab",)
    list_per_page = 20
admin.site.register(models.OutfitItem, OutfitItemAdmin)

class CharadesWordsAdmin(admin.ModelAdmin):
    list_display = ("EN_US",)
    search_fields = ("EN_US",)
    list_filter = ("Difficulty",)
    list_per_page = 20
admin.site.register(models.CharadesWords, CharadesWordsAdmin)

admin.site.register(models.LevelProgressionMap)
admin.site.register(models.Ban)

class GiftDropAdmin(admin.ModelAdmin):
    list_display = ("FriendlyName", "Rarity", "Context")
    search_fields = ("FriendlyName",)
    list_filter = ("Rarity", "Context")
    list_per_page = 20
    #autocomplete_fields = ("Equipment","OutfitItem")
admin.site.register(models.GiftDrop, GiftDropAdmin)

class ChallengeMapAdmin(admin.ModelAdmin):
    list_display = ("StartAt", "EndAt")
    search_fields = ()
    list_filter = ()
    list_per_page = 20
    filter_horizontal = ("Challenges","GiftsDrops")
admin.site.register(models.ChallengeMap, ChallengeMapAdmin)

admin.site.register(models.Gift)
admin.site.register(models.MyGiGiftDrop)
admin.site.register(models.Relationship)
admin.site.register(models.PlayerEmail)