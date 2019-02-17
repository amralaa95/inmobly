# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils import create_videos_list
from oauth2client.contrib.django_util.models import CredentialsField

class CredentialsModel(models.Model):
    credential = CredentialsField()

class YoutubeSource(models.Model):
    TYPE_CHANNEL = 1
    TYPE_PLAYLIST = 2

    TYPES_CHOICES = (
        (TYPE_CHANNEL, ('Channel')),
        (TYPE_PLAYLIST, ('Playlist'))
    )
    name = models.CharField(max_length=250)
    type = models.SmallIntegerField(choices=TYPES_CHOICES)
    
class Video(models.Model):
    name = models.CharField(max_length=250)
    title = models.CharField(max_length=250)
    duration = models.CharField(max_length = 15)
    views = models.IntegerField()
    thumbnail_image = models.ImageField(upload_to = 'media')
    original_image = models.ImageField(upload_to='media')
    thumbnail_url = models.CharField(max_length = 300)
    original_url = models.CharField(max_length = 300)
    fk_source = models.ForeignKey(YoutubeSource, on_delete=models.CASCADE)
   
@receiver(post_save, sender=YoutubeSource)
def auto_create_videos(sender, instance, **kwargs):
    create_videos_list(instance)


