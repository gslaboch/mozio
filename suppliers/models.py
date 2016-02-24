from __future__ import unicode_literals

from django.contrib.gis.db import models
from django.conf.global_settings import LANGUAGES

class Provider(models.Model):
    CURRENCY_CHOICES = (
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
    )
        
    name = models.CharField(max_length=80)
    email = models.CharField(max_length=80)
    phone = models.CharField(max_length=30)
    language = models.CharField(max_length=7, choices = LANGUAGES, default = 'en')
    currency = models.CharField(max_length=3, choices = CURRENCY_CHOICES, default = 'USD')
    
    def __unicode__(self):
        return self.name
    
class ServiceArea(models.Model):
    
    name = models.CharField(max_length=80)
    price = models.DecimalField(max_digits = 12, decimal_places = 2)
    poly = models.MultiPolygonField()
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.name
