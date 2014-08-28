
from django.contrib.gis.db import models as gis_models
from django.contrib.gis import geos
from django.db import models

import pytz
import datetime
from django.utils import timezone


class account(models.Model):
     twitterid = models.BigIntegerField()
     credit    = models.BigIntegerField(default = 0)
     speakcounter = models.BigIntegerField(default = 0)
     balance = models.BigIntegerField(default = 0)
     followers    = models.BigIntegerField(blank=True)
     password = models.CharField(max_length=500,blank=True)
     showonmap = models.CharField(max_length=500,default="no")
     bio = models.TextField(max_length=1000,blank=True)
     username = models.CharField(max_length=100)
     name = models.CharField(max_length=100, blank=True)
     image = models.TextField(max_length=1000,blank=True)
     delacc  = models.TextField(blank=True)
     language = models.CharField(max_length=500,blank=True)
     email = models.EmailField(max_length=300,blank=True)
     pro = models.CharField(max_length=500 , blank=True)
     status = models.CharField(max_length=500 , blank=True)
     
     regdate = models.DateField(auto_now_add=True)
     location = gis_models.PointField(u"longitude/latitude", geography=True, blank=True, null=True)
     gis = gis_models.GeoManager()
     objects = models.Manager()
    
     def __unicode__(self):
          return self.username

    