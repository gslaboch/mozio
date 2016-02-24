from django.contrib.gis.geos import Point
from rest_framework import routers, serializers, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from models import Provider, ServiceArea
from serializers import *


class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    
class ServiceAreaViewSet(viewsets.ModelViewSet):
    queryset = ServiceArea.objects.all()
    serializer_class = ServiceAreaSerializer

    @list_route(methods=['get', 'post'], url_path='check')
    def check(self, request, format=None):
        try:
            if request.method == 'GET':
                lat = float(request.query_params['lat'])
                lon = float(request.query_params['lon'])
            else:
                lat = float(request.data['lat'])
                lon = float(request.data['lon'])
            
        except ValueError:
            raise serializers.ValidationError("Lat/Lon format is invalid")
        except KeyError:
            raise serializers.ValidationError("Both 'lat' and 'lon' parameters are required")
            
        
        point = Point((float(lon), float(lat)))
        areas = ServiceArea.objects.filter(poly__contains=point).all()
        #TODO: If database is MYSQL, the operation is done on bounding boxs, so we need to manually re-check 
        serializer = ServiceAreaSerializer(areas, many=True, context={'request': request})
        return Response(serializer.data)
    
router = routers.DefaultRouter()
router.register(r'provider', ProviderViewSet)
router.register(r'servicearea', ServiceAreaViewSet)
