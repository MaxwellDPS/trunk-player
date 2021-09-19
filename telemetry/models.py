import json
import logging
import uuid
import urllib.parse

from django.db import models
from datetime import timedelta
from django.db.models.deletion import CASCADE
from django.db.models.fields import DateField
from django.utils import timezone
from django.utils.text import slugify
from django.conf import settings
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.utils import OperationalError

from radio.models import System

log = logging.getLogger(__name__)


class Source(models.Model):
    source = models.IntegerField()
    signal_system = models.CharField(max_length=50)
    emergency = models.BooleanField(default=False)

    def __str__(self):
        return f"[{self.signal_system}] {str(self.source)}"

class Freq(models.Model):
    freq = models.IntegerField()

    def __str__(self):
        return str(self.freq/1000000)

class Call(models.Model):
    call_id = models.CharField(unique=True, max_length=255)
    freq = models.IntegerField()
    sysNum = models.IntegerField()
    shortName = models.CharField(max_length=255)
    talkgroup =  models.IntegerField()
    talkgrouptag = models.CharField(max_length=255)
    elasped =  models.IntegerField()
    length =  models.IntegerField()
    state =  models.IntegerField()
    recNum =  models.IntegerField()
    srcNum =  models.IntegerField()
    recState =  models.IntegerField()
    sigmffilename = models.TextField()
    debugfilename = models.TextField()
    filename = models.TextField()
    statusfilename = models.TextField()
    startTime = models.DateTimeField()
    stopTime = models.DateTimeField()
    phase2 = models.BooleanField(default=False)
    conventional = models.BooleanField(default=False)
    encrypted = models.BooleanField(default=False)
    emergency = models.BooleanField(default=False)
    analog = models.BooleanField(default=False)


    sourceList = models.ManyToManyField(Source)
    freqList = models.ManyToManyField(Freq)

    def __str__(self):
        return f"[{self.call_id}] {self.talkgrouptag}"

class SystemStatus(models.Model):
    system =  models.ForeignKey(System, unique=True, on_delete=CASCADE)

    activeCalls = models.ManyToManyField(Call)
    decoderate = models.IntegerField(null=True, blank=True)


    def __str__(self):
        return str(self.system)
