from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.gis.geos import GEOSGeometry
from models import Provider, ServiceArea
from rest_framework.test import APITransactionTestCase, APITestCase
from rest_framework import status
from decimal import Decimal
import json


class AuthenticatedTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="test-user", password="123456", is_superuser=True)
        self.client.force_authenticate(self.user)


class ProviderTests(AuthenticatedTestCase):

    def test_create_provider(self):
        """
        Ensure we can create a new Provider
        """
        url = reverse('provider-list')
        data = {
                "name": "Test User",
                "email": "testuser@email.com",
                "phone": "+54912345678",
                "language": "en",
                "currency": "USD",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_id = response.data.get("id", None)
        self.assertNotEqual(created_id, None)

        provider = Provider.objects.get(pk=created_id)
        self.assertEqual(provider.name, data["name"])
        self.assertEqual(provider.email, data["email"])
        self.assertEqual(provider.phone, data["phone"])
        self.assertEqual(provider.language, data["language"])
        self.assertEqual(provider.currency, data["currency"])

    def test_get_provider(self):
        """
        Ensure we can get a provider
        """

        provider = Provider.objects.create(name="Gonza", email="gonza@email.com", phone="+5491234567",
                                           language="en", currency="USD")

        url = reverse('provider-detail', args=[provider.id])
        response = self.client.get(url, format='json')
        self.assertTrue(status.is_success(response.status_code))

        self.assertEqual(provider.name, response.data["name"])
        self.assertEqual(provider.email, response.data["email"])
        self.assertEqual(provider.phone, response.data["phone"])
        self.assertEqual(provider.language, response.data["language"])
        self.assertEqual(provider.currency, response.data["currency"])

    def test_delete_provider(self):
        """
        Ensure we can delete a provider.
        """

        provider = Provider.objects.create(name="User To Delete", email="user-to-delete@email.com", phone="+5491234567",
                                           language="en", currency="USD")

        url = reverse('provider-detail', args=[provider.id])
        response = self.client.delete(url)

        self.assertTrue(status.is_success(response.status_code))

        with self.assertRaises(ObjectDoesNotExist):
            Provider.objects.get(pk=provider.id)

    def test_get_provider_list(self):
        """
        Ensure we can get the list of providers
        """

        Provider.objects.create(name="Gonza", email="gonza@email.com", phone="+5491234567",
                                language="en", currency="USD")
        Provider.objects.create(name="Pablo", email="pablo@email.com", phone="+5499876543",
                                language="es", currency="EUR")

        url = reverse('provider-list')
        response = self.client.get(url, format='json')

        self.assertTrue(status.is_success(response.status_code))
        self.assertEquals(len(response.data), 2)


class ServiceAreaTests(AuthenticatedTestCase):

    def get_concave_polygon_json(self):
        return {
            "type": "MultiPolygon",
            "coordinates": [
                [
                    [
                        [
                            -60.72009254065352,
                            -31.631847952999507
                        ],
                        [
                            -60.73073554602263,
                            -31.641786206648828
                        ],
                        [
                            -60.72713065710748,
                            -31.653330785209405
                        ],
                        [
                            -60.70601630774467,
                            -31.657568308709024
                        ],
                        [
                            -60.67494559852067,
                            -31.641347776676408
                        ],
                        [
                            -60.679752117074514,
                            -31.622493332416735
                        ],
                        [
                            -60.69674659339055,
                            -31.640178619976822
                        ],
                        [
                            -60.71047950354497,
                            -31.637255663913102
                        ],
                        [
                            -60.702926402960266,
                            -31.614892010644162
                        ],
                        [
                            -60.7199208792763,
                            -31.613576334235333
                        ],
                        [
                            -60.72009254065352,
                            -31.631847952999507
                        ]
                    ]
                ]
            ]
        }

    def test_create_service_area(self):
        """
        Ensure we can create a new service area.
        """

        provider = Provider.objects.create(name="Gonza", email="gonza@email.com", phone="+5491234567",
                                           language="en", currency="USD")
        data = {
            "name": "Santa Fe Concave",
            "price": Decimal("1000.00"),
            "poly": self.get_concave_polygon_json(),
            "provider": provider.id
        }
        url = reverse('servicearea-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_id = response.data.get("id", None)
        self.assertNotEqual(created_id, None)

        area = ServiceArea.objects.get(pk=created_id)
        self.assertEqual(area.name, data["name"])
        self.assertEqual(area.price, data["price"])
        self.assertEqual(area.provider.id, data["provider"])

    def test_check_inside_service_area(self):
        """
        Ensure we can get a service area, using a point that is inside of it.
        """

        provider = Provider.objects.create(name="Gonza", email="gonza@email.com", phone="+5491234567",
                                           language="en", currency="USD")
        servicearea = {
            "name": "Santa Fe Concave",
            "price": Decimal("1000.00"),
            "poly": GEOSGeometry(json.dumps(self.get_concave_polygon_json())),
            "provider": provider
        }
        area = ServiceArea.objects.create(**servicearea)

        url = reverse('servicearea-list') + "check/"
        response = self.client.get(url, {'lat': '-31.645', 'lon': '-60.70'}, format='json')

        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(len(response.data['features']), 1)

        properties = response.data['features'][0]['properties']
        self.assertEqual(area.name, properties['name'])

    def test_check_outside_service_area(self):
        """
        Ensure we can get a service area, using a point that is inside of it.
        Test on a concave polygon, in a point inside the bounding box, but outside
        de polygon. This is important for databases that do not fully implement
        spatial operations
        """

        provider = Provider.objects.create(name="Gonza", email="gonza@email.com", phone="+5491234567",
                                           language="en", currency="USD")
        servicearea = {
            "name": "Santa Fe Concave",
            "price": Decimal("1000.00"),
            "poly": GEOSGeometry(json.dumps(self.get_concave_polygon_json())),
            "provider": provider
        }
        area = ServiceArea.objects.create(**servicearea)

        url = reverse('servicearea-list') + "check/"
        response = self.client.get(url, {'lat': '-31.628', 'lon': '-60.697'}, format='json')

        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(len(response.data['features']), 0)
