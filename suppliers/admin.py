from django.contrib import admin
from django.contrib.gis.admin import GeoModelAdmin
from .models import Provider, ServiceArea


class ServiceAreaAdmin(GeoModelAdmin): 
    default_lat = -31.6
    default_lon = -60.7

admin.site.register(Provider)
admin.site.register(ServiceArea, ServiceAreaAdmin)