from modulefinder import AddPackagePath
from msilib.schema import AppSearch
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.contrib.auth.models import User
import os

# Create your models here.
class Level(models.Model):
    PREMIER = 'PREMIER'
    DIVISION_I = 'DIVISION I'
    DIVISION_II = 'DIVISION II'
    
    LEVEL_TYPE_CHOICES = [
        (PREMIER, 'Premier'),
        (DIVISION_I, 'Division I'),
        (DIVISION_II, 'Division II'),
    ]

    GENDER_CHOICES = [
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
    ]

    level_type = models.CharField(max_length=15, choices=LEVEL_TYPE_CHOICES, unique=True, default=PREMIER)
    slug = models.SlugField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='MALE')

    def __str__(self):
        return self.level_type

    def save(self, *args, **kwargs):
        self.slug = slugify(self.level_type)
        super().save(*args, **kwargs)

def save_team_image(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.team_id:
        filename = 'Team_Pictures/{}.{}'.format(instance.team_id, ext)
    return os.path.join(upload_to, filename)

class Team(models.Model):
    team_id = models.CharField(max_length=100, unique=True)
    team_name = models.CharField(max_length=100)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='teams')
    slug = models.SlugField(null=True, blank=True)
    description = models.TextField(max_length=500,blank=True)
    image = models.ImageField(upload_to=save_team_image, blank=True, verbose_name='Team Image')
    hometown = models.CharField(max_length=100)

    def __str__(self):
        return self.team_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.team_name)
        super().save(*args, **kwargs)

def save_player_image(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.player_id:
        filename = 'Player_Pictures/{}.{}'.format(instance.player_id, ext)
    return os.path.join(upload_to, filename)

def save_player_files(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.lesson_id:
        filename = 'player_files/{}/{}.{}'.format(instance.player_id,instance.player_id, ext)
        if os.path.exists(filename):
            new_name = str(instance.player_id) + str('1')
            filename =  'player_images/{}/{}.{}'.format(instance.player_id,new_name, ext)
    return os.path.join(upload_to, filename)

class Player(models.Model):
    GENDER_CHOICES = [
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
    ]
    player_id = models.CharField(max_length=100, unique=True)
    player_height = models.IntegerField(blank=True)
    player_weight = models.IntegerField(blank=True)
    player_age = models.IntegerField(blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE,related_name='players')
    player_name = models.CharField(max_length=250)
    player_position = models.CharField(max_length=100, verbose_name="position")
    slug = models.SlugField(null=True, blank=True)
    video = models.FileField(upload_to=save_player_files,verbose_name="Video", blank=True, null=True)
    player_image = models.ImageField(upload_to=save_player_image,verbose_name="Player ProfilePics", blank=True)
    player_stats = models.FileField(upload_to=save_player_files,verbose_name="Stats", blank=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='MALE')
    

    
    def __str__(self):
        return self.player_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.player_name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('league:player_list', kwargs={'slug':self.team.slug, 'level':self.Level.slug})

class Stats(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='pstats')
    ppg=models.PositiveSmallIntegerField()
    rpg=models.PositiveSmallIntegerField()
    apg=models.PositiveSmallIntegerField()
    spg=models.PositiveSmallIntegerField()


    class Meta:
        ordering = ('-ppg', 'player')#creating the leaderboard for points, hyphen used for the descending order

    def __int__(self):
        return self.ppg

    def save(self, *args, **kwargs):
        self.slug = slugify(self.ppg)
        super().save(*args, **kwargs)