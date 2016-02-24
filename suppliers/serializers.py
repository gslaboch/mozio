from rest_framework.serializers import HyperlinkedModelSerializer
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from models import Provider, ServiceArea


class ProviderSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Provider
        fields = ('id', 'name', 'email', 'phone', 'language', 'currency')


class ServiceAreaSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = ServiceArea
        geo_field = 'poly'
        fields = ('id', 'name', 'price', 'provider')
