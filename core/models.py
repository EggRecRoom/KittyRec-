from django.db import models
from . import enums

# Create your models here.

class Player(models.Model):
    Username = models.CharField(max_length=100, unique=True)
    DisplayName = models.CharField(max_length=100)
    Password = models.CharField(max_length=4000, null=True, blank=True, default=None)
    Email = models.EmailField(null=True, blank=True)
    XP = models.IntegerField(default=0)
    Level = models.IntegerField(default=1)
    Reputation = models.IntegerField(default=0)
    Verified = models.BooleanField(default=False)
    Developer = models.BooleanField(default=False)
    CanReceiveInvites = models.BooleanField(default=False)
    ProfileImage = models.ImageField(upload_to='profile_images/', null=True, blank=True, default='profile_images/DefaultProfileImage.png')

    def __str__(self):
        return self.Username
    
class Login(models.Model):
    Platform = models.IntegerField(choices=enums.PlatformType.choices, default=enums.PlatformType.STEAM)
    PlatformId = models.CharField(max_length=100)
    Player = models.ForeignKey(Player, on_delete=models.CASCADE)
    LastLoginDateTime = models.DateTimeField()


    def __str__(self):
        Platform = enums.PlatformType(self.Platform)
        if Platform == enums.PlatformType.STEAM:
            PlatformName = "Steam"
        elif Platform == enums.PlatformType.OCULUS:
            PlatformName = "Oculus"
        elif Platform == enums.PlatformType.PS4:
            PlatformName = "PlayStation 4"
        elif Platform == enums.PlatformType.MICROSOFT:
            PlatformName = "Microsoft"
        else:
            PlatformName = "Unknown"
        return f"{self.Player.Username} - {PlatformName} - {self.PlatformId}"
    

class PlayerPresence(models.Model):
    Player = models.ForeignKey(Player, on_delete=models.CASCADE)
    IsOnline = models.BooleanField(default=False)
    GameSessionId = models.CharField(max_length=100, null=True, blank=True)
    AppVersion = models.CharField(max_length=100, null=True, blank=True)
    Activity = models.CharField(max_length=100, null=True, blank=True)
    Private = models.BooleanField(default=False)
    AvailableSpace = models.IntegerField(default=0)
    GameInProgress = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.Player.Username} - {'Online' if self.IsOnline else 'Offline'} - {self.Activity}"
    

class message(models.Model):
    Sender = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='sent_messages')
    Receiver = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='received_messages')
    SentTime = models.DateTimeField(auto_now_add=True)
    Type = models.IntegerField(choices=enums.MessageType.choices)
    Data = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return f"Message from {self.Sender.Username} to {self.Receiver.Username} - {self.Type} - {self.SentTime}"
    
class Avatar(models.Model):
    Player = models.ForeignKey(Player, on_delete=models.CASCADE)
    OutfitSelections = models.CharField(max_length=1000, null=True, blank=True)
    HairColor = models.CharField(max_length=1000, null=True, blank=True)
    SkinColor = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return f"Avatar for {self.Player.Username} - Outfit: {self.OutfitSelections} - Hair: {self.HairColor} - Skin: {self.SkinColor}"
    
class Setting(models.Model):
    Player = models.ForeignKey(Player, on_delete=models.CASCADE)
    Key = models.CharField(max_length=100)
    Value = models.CharField(max_length=1000)

    def __str__(self):
        return f"Setting for {self.Player.Username} - {self.Key}: {self.Value}"
    
class Event(models.Model):
    Name = models.CharField(max_length=100)
    Description = models.TextField(max_length=3000)
    StartTime = models.DateTimeField()
    EndTime = models.DateTimeField()
    Activity = models.IntegerField(choices=enums.ActivityType.choices, default=enums.ActivityType.INVALID)
    ActivityLevel = models.IntegerField(choices=enums.ActivityLevelType.choices, default=enums.ActivityLevelType.INVALID)
    PosterImage = models.ImageField(upload_to='event_posters/')
    GameSessionId = models.CharField(max_length=100)
    MaxPlayers = models.IntegerField(default=0)
    CreatorPlayer = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='created_events', null=True, blank=True)

    def __str__(self):
        return f"Event: {self.Name} - {self.Description} - {self.StartTime} to {self.EndTime} - Activity: {self.Activity} - Level: {self.ActivityLevel}"
    
class DynamicPoster(models.Model):
    Name = models.CharField(max_length=100)
    Image = models.ImageField(upload_to='dynamic_posters/')

    def __str__(self):
        return f"{self.Name}"


class Equipment(models.Model):
    FriendlyName = models.CharField(max_length=100)
    PrefabName = models.CharField(max_length=100)
    ModificationGuid = models.CharField(max_length=100)
    UnlockedLevel = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.FriendlyName}"


class PlayerImage(models.Model):
    Player = models.ForeignKey(Player, on_delete=models.CASCADE)
    Image = models.ImageField(upload_to='player_images/')
    GameSessionId = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.Player.Username} - {self.GameSessionId}"
    
class Relationship(models.Model):
    Player1 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="Player")
    Player2 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="PlayerShip")
    RelationshipType = models.IntegerField(choices=enums.RelationshipType.choices, default=enums.RelationshipType.None_)
    Mute = models.BooleanField(default=False)
    Ignore = models.BooleanField(default=False)

#class Report(models.Model):
#    Player = models.ForeignKey(Player, on_delete=models.CASCADE)
#    ReportedPlayer = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='reported_player')
#    ReportCategory = models.IntegerField(choices=enums.ReportCategory.choices, default=enums.ReportCategory.Unknown)
#    Activity = models.CharField(max_length=1000, null=True, blank=True)

class HowToVideo(models.Model):
    Video = models.FileField(upload_to='video/')
    PlayButtonImage = models.ImageField(upload_to='video_image/', null=True, blank=True)
    Volume = models.FloatField(default=0.1)
    PitchVariation = models.FloatField(default=0.0)
    PitchShift = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.Video.name.replace("video/", "")} - {self.PlayButtonImage.name} - Volume: {self.Volume} - PitchVariation: {self.PitchVariation} - PitchShift: {self.PitchShift}"

class Radio(models.Model):
    audio = models.FileField(upload_to='audio/')
    AudioType = models.IntegerField(choices=enums.AudioType.choices, default=enums.AudioType.OGGVORBIS)

    def __str__(self):
        return f"{self.audio.name.replace("audio/", "")}"
    
class OutfitItem(models.Model):
    friendlyName = models.CharField(max_length=100)
    prefab = models.CharField(choices=enums.OutfitItemPrefab.choices, default=enums.OutfitItemPrefab.Hat_Angler, max_length=300)
    colorSwatch = models.CharField(max_length=100, null=True, blank=True)
    mask = models.CharField(max_length=100, null=True, blank=True)
    decal = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.friendlyName}"


class GiftDrop(models.Model):
    FriendlyName = models.CharField(max_length=100)
    Context = models.IntegerField(choices=enums.Context.choices, default=enums.Context.None_) 
    Rarity = models.IntegerField(choices=enums.Rarity.choices, default=enums.Rarity.Common)
    Xp = models.IntegerField(default=0)
    OutfitItem = models.ForeignKey(OutfitItem, on_delete=models.CASCADE, null=True, blank=True)
    Equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, null=True, blank=True)
 
    def __str__(self):
        return f"{self.FriendlyName}"

class CharadesWords(models.Model):
    EN_US = models.CharField(max_length=100)
    Difficulty = models.IntegerField(choices=enums.CharadesDifficulty.choices, default=enums.CharadesDifficulty.EASY)

class LevelProgressionMap(models.Model):
    Level = models.IntegerField(default=0)
    RequiredXp = models.IntegerField(default=0)

class Ban(models.Model):
    Player = models.ForeignKey(Player, on_delete=models.CASCADE)
    ReportCategory = models.IntegerField(choices=enums.ReportCategory.choices, default=enums.ReportCategory.Unknown)
    StartAt = models.DateTimeField(auto_now_add=True)
    EndAt = models.DateTimeField()
    Reason = models.CharField(max_length=1000, null=True, blank=True)

class Challenge(models.Model):
    Name = models.CharField(max_length=100)

class ChallengeMap(models.Model):
    StartAt = models.DateTimeField()
    EndAt = models.DateTimeField()
    Challenges = models.ManyToManyField(Challenge, blank=True)
    GiftsDrops = models.ManyToManyField(GiftDrop, blank=True)

class Gift(models.Model):
    Player = models.ForeignKey(Player, on_delete=models.CASCADE)
    SentAt = models.DateTimeField(auto_now_add=True)
    GiftDrop = models.ForeignKey(GiftDrop, on_delete=models.CASCADE)
    Message = models.CharField(max_length=1000)
    Opened = models.BooleanField(default=False)

    def __str__(self):
        return f"Gift from {self.Player.Username}"
    
class MyGiGiftDrop(models.Model):
    Player = models.ForeignKey(Player, on_delete=models.CASCADE)
    GiftDrop = models.ForeignKey(GiftDrop, on_delete=models.CASCADE)
    AddedAt = models.DateTimeField(auto_now_add=True)

class PlayerEmail(models.Model):
    Code = models.CharField(max_length=300)
    Player = models.ForeignKey(Player, on_delete=models.CASCADE)
    Email = models.EmailField()
    Used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.Email}"