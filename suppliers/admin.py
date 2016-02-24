from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Provider, ServiceArea


class ServiceAreaAdmin(OSMGeoAdmin): 
    max_extent = False
    default_lat = -31.6
    default_lon = -60.7
    display_srid = 4326

admin.site.register(Provider)
admin.site.register(ServiceArea, ServiceAreaAdmin)