from rest_framework import routers, serializers, viewsets
from models import Provider, ServiceArea
from serializers import *


        
class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    
class ServiceAreaViewSet(viewsets.ModelViewSet):
    queryset = ServiceArea.objects.all()
    serializer_class = ServiceAreaSerializer

    
router = routers.DefaultRouter()
router.register(r'provider', ProviderViewSet)
router.register(r'servicearea', ServiceAreaViewSet)
