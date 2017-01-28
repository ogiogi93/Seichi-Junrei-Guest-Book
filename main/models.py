from __future__ import unicode_literals

from django.db import models
import datetime


class Face(models.Model):
    id = models.AutoField(primary_key=True)
    face_id = models.CharField(max_length=255, blank=False)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    path = models.ImageField(upload_to='face', blank=True, default='face/default.png')


class PersistedFace(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(default=datetime.datetime.now())
    persisted_id = models.CharField(max_length=255, blank=False)
    path = models.ImageField(upload_to='picture', blank=True, default='picture/default.png')
