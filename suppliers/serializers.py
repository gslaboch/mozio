from rest_framework import serializers
from models import Provider, ServiceArea

class ProviderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Provider
        fields = ('id' , 'name', 'email', 'phone', 'language', 'currency')
        
        
class ServiceAreaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ServiceArea
        fields = ('name', 'price', 'poly', 'provider')