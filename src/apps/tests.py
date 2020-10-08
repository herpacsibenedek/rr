import logging

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from .models import Partner, Auto, AutoPartnerConnection
from .serializers import (
    PartnerSerializer,
    AutoSerializer
)

User = get_user_model()

# Disable logger for tests
logging.disable(logging.CRITICAL)


class LoginTest(APITestCase):
    """
    Test Module for login endpoint
    """

    def setUp(self):
        self.user = User.objects.create_user(username="user1", email="user1@test.com", password="password1")
        self.client = APIClient()

    def test_login(self):
        url = reverse('login')
        data = {
            "username": "user1",
            "password": "password1"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_invalid(self):
        url = reverse('login')
        data = {
            "username": "user1123",
            "password": "password1"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PartnerCreateTest(APITestCase):
    """
    Test Module for partner create
    """

    def setUp(self):
        self.user = User.objects.create_user(username="user1", email="user1@test.com", password="password1")
        self.client = APIClient()

    def test_create_no_auth(self):
        """
        Ensure we cannot create a new partner object without authentication.
        """
        url = reverse('partner-list')
        data = {
            "name": "name",
            "city": "city",
            "address": "address",
            "company_name": "company_name"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_partner(self):
        """
        Ensure we can create a new partner object.
        """
        url = reverse('partner-list')
        data = {
            "name": "name",
            "city": "city",
            "address": "address",
            "company_name": "company_name"
        }
        self.client.force_authenticate(self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Partner.objects.count(), 1)
        self.assertEqual(Partner.objects.first().name, 'name')
        self.assertEqual(Partner.objects.first().city, 'city')
        self.assertEqual(Partner.objects.first().address, 'address')
        self.assertEqual(Partner.objects.first().company_name, 'company_name')

    def test_create_partner_require_name(self):
        """
        Ensure we cannot create an invalid partner object.
        """
        url = reverse('partner-list')
        data = {
            "city": "city",
            "address": "address",
            "company_name": "company_name"
        }
        self.client.force_authenticate(self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_partner_require_city(self):
        """
        Ensure we cannot create an invalid partner object.
        """
        url = reverse('partner-list')
        data = {
            "name": "name",
            "address": "address",
            "company_name": "company_name"
        }
        self.client.force_authenticate(self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_partner_require_address(self):
        """
        Ensure we cannot create an invalid partner object.
        """
        url = reverse('partner-list')
        data = {
            "name": "name",
            "city": "city",
            "company_name": "company_name"
        }
        self.client.force_authenticate(self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_partner_require_company(self):
        """
        Ensure we cannot create an invalid partner object.
        """
        url = reverse('partner-list')
        data = {
            "name": "name",
            "city": "city",
            "address": "address"
        }
        self.client.force_authenticate(self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PartnerGetAllTest(APITestCase):
    """
    Test module for GET all partners
    """

    def setUp(self):
        self.user = User.objects.create_user(username="user1", email="user1@test.com", password="password1")
        self.client = APIClient()

    def setup_partners(self):
        Partner.objects.create(
            name='Bolt1', city='LA', address='4035 Cím utca 8', company_name='Bolt1')
        Partner.objects.create(
            name='Bolt2', city='LA', address='4035 Cím utca 8', company_name='Bolt1')
        Partner.objects.create(
            name='Bolt3', city='LA', address='4035 Cím utca 8', company_name='Bolt1')
        Partner.objects.create(
            name='Bolt4', city='LA', address='4035 Cím utca 8', company_name='Bolt1')

    def test_get_all_partners_no_auth(self):
        """
        Test module for GET all partners without authnetication
        """
        self.setup_partners()
        response = self.client.get(reverse('partner-list'))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all_partners(self):
        """
        Test module for GET all partners
        """
        self.setup_partners()
        self.client.force_authenticate(self.user)
        response = self.client.get(reverse('partner-list'))

        partnerek = Partner.objects.all()
        serializer = PartnerSerializer(partnerek, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_partners_nested(self):
        self.setup_partners()
        self.client.force_authenticate(self.user)
        response = self.client.get(
            reverse('partner-list'),
            {'query': 'nested'}
        )

        partnerek = Partner.objects.all()
        serializer = PartnerSerializer(partnerek, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_partners_flat(self):
        self.setup_partners()
        self.client.force_authenticate(self.user)
        response = self.client.get(
            reverse('partner-list'),
            {'query': 'NOt nested'}
        )

        partnerek = Partner.objects.all()
        serializer = PartnerSerializer(partnerek, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PartnerGetSingleTest(APITestCase):
    """
    Test module for GET a partner
    """

    def setUp(self):
        self.user = User.objects.create_user(username="user1", email="user1@test.com", password="password1")
        self.client = APIClient()

    def setup_partners(self):
        Partner.objects.create(
            name='Bolt1', city='LA', address='4035 Cím utca 8', company_name='Bolt1')
        self.partner = Partner.objects.create(
            name='Bolt2', city='LA', address='4035 Cím utca 8', company_name='Bolt1')
        Partner.objects.create(
            name='Bolt3', city='LA', address='4035 Cím utca 8', company_name='Bolt1')
        Partner.objects.create(
            name='Bolt4', city='LA', address='4035 Cím utca 8', company_name='Bolt1')

    def test_get_single_partner_no_auth(self):
        """
        Test module for GET a partner without authentication
        """
        self.setup_partners()
        response = self.client.get(
            reverse('partner-detail', kwargs={'pk': self.partner.id})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_single_partner(self):
        """
        Test module for GET a partner
        """
        self.setup_partners()
        self.client.force_authenticate(self.user)
        response = self.client.get(
            reverse('partner-detail', kwargs={'pk': self.partner.id})
        )

        serializer = PartnerSerializer(self.partner)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_partner_invalid_id(self):
        """
        Test module for GET a partner with Invalid ID
        """
        self.setup_partners()
        self.client.force_authenticate(self.user)
        response = self.client.get(
            reverse('partner-detail', kwargs={'pk': 99})
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_single_partner_nested(self):
        self.setup_partners()
        self.client.force_authenticate(self.user)
        response = self.client.get(
            reverse('partner-detail', kwargs={'pk': self.partner.id}),
            {'query': 'nested'}
        )

        serializer = PartnerSerializer(self.partner)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_partner_flat(self):
        self.setup_partners()
        self.client.force_authenticate(self.user)
        response = self.client.get(
            reverse('partner-detail', kwargs={'pk': self.partner.id}),
            {'query': 'nopenested'}
        )

        serializer = PartnerSerializer(self.partner)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PartnerDeleteTest(APITestCase):
    """
    Test module for deleting an existing partner
    """

    def setUp(self):
        self.user = User.objects.create_user(username="user1", email="user1@test.com", password="password1")
        self.client = APIClient()
        self.partner = Partner.objects.create(
            name='Bolt', city='LA', address='4035 Cím utca 8', company_name='Bolt')
        Partner.objects.create(
            name='Bolt2', city='LA', address='4035 Cím utca 8', company_name='Bolt')

    def test_partner_delete(self):
        """
        Test module for deleting an existing partner
        """
        self.client.force_authenticate(self.user)
        response = self.client.delete(
            reverse('partner-detail', kwargs={'pk': self.partner.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Partner.objects.count(), 2)
        self.assertNotEqual(Partner.objects.first().deleted_at, None)

        # Check get a single partner
        response = self.client.delete(
            reverse('partner-detail', kwargs={'pk': self.partner.id})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Check get list
        response = self.client.get(reverse('partner-list'))
        partnerek = Partner.objects.filter(deleted_at=None)
        serializer = PartnerSerializer(partnerek, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(Partner.objects.count(), 2)

    def test_partner_delete_no_auth(self):
        response = self.client.delete(
            reverse('partner-detail', kwargs={'pk': self.partner.id})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partner_delete_invalid_id(self):
        self.client.force_authenticate(self.user)
        response = self.client.delete(
            reverse('partner-detail', kwargs={'pk': 99})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AutoCreateTest(APITestCase):
    """
    Ensure we can create a new auto object.
    """

    def setUp(self):
        self.user = User.objects.create_user(username="user1", email="user1@test.com", password="password1")
        self.client = APIClient()

    def test_create_no_auth(self):
        """
        Ensure we cannot create a new auto object without authentication.
        """
        url = reverse('auto-list')
        data = {
            "average_fuel": "12.3",
            "delegation_starting": "0",
            "delegation_ending": "123",
            "driver": "Bela",
            "owner": "Bela",
            "type": "Magán"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_auto(self):
        """
        Ensure we can create a new auto object.
        """
        url = reverse('auto-list')
        data = {
            "average_fuel": "12.3",
            "delegation_starting": "0",
            "delegation_ending": "123",
            "driver": "Bela",
            "owner": "Bela",
            "type": "Magán"
        }
        self.client.force_authenticate(self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Auto.objects.count(), 1)
        self.assertEqual(float(Auto.objects.first().average_fuel), float(12.3))
        self.assertEqual(Auto.objects.first().delegation_starting, 0)
        self.assertEqual(Auto.objects.first().delegation_ending, 123)
        self.assertEqual(Auto.objects.first().driver, 'Bela')
        self.assertEqual(Auto.objects.first().owner, 'Bela')
        self.assertEqual(Auto.objects.first().type, 'Magán')

    def test_create_auto_require_average_fuel(self):
        """
        Ensure we cannot create an invalid auto object.
        """
        url = reverse('auto-list')
        data = {
            "delegation_starting": "0",
            "delegation_ending": "123",
            "driver": "Bela",
            "owner": "Bela",
            "type": "Magán",
        }
        self.client.force_authenticate(self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_auto_require_delegation_starting(self):
        """
        Ensure we cannot create an invalid auto object.
        """
        url = reverse('auto-list')
        data = {
            "average_fuel": "12.3",
            "delegation_ending": "123",
            "driver": "Bela",
            "owner": "Bela",
            "type": "Magán",
        }
        self.client.force_authenticate(self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_auto_require_delegation_ending(self):
        """
        Ensure we cannot create an invalid auto object.
        """
        url = reverse('auto-list')
        data = {
            "average_fuel": "12.3",
            "delegation_starting": "0",
            "driver": "Bela",
            "owner": "Bela",
            "type": "Magán",
        }
        self.client.force_authenticate(self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_auto_require_driver(self):
        """
        Ensure we cannot create an invalid auto object.
        """
        url = reverse('auto-list')
        data = {
            "average_fuel": "12.3",
            "delegation_starting": "0",
            "delegation_ending": "123",
            "owner": "Bela",
            "type": "Magán",
        }
        self.client.force_authenticate(self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_auto_require_owner(self):
        """
        Ensure we cannot create an invalid auto object.
        """
        url = reverse('auto-list')
        data = {
            "average_fuel": "12.3",
            "delegation_starting": "0",
            "delegation_ending": "123",
            "driver": "Bela",
            "type": "Magán",
        }
        self.client.force_authenticate(self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_auto_require_type(self):
        """
        Ensure we cannot create an invalid auto object.
        """
        url = reverse('auto-list')
        data = {
            "average_fuel": "12.3",
            "delegation_starting": "0",
            "delegation_ending": "123",
            "driver": "Bela",
            "owner": "Bela"
        }
        self.client.force_authenticate(self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AutoGetAllTest(APITestCase):
    """
    Test module for GET all auto
    """

    def setUp(self):
        self.user = User.objects.create_user(username="user1", email="user1@test.com", password="password1")
        self.client = APIClient()

    def setup_autok(self):
        Auto.objects.create(
            average_fuel=12.3,
            delegation_starting=0,
            delegation_ending=123,
            driver='Bela',
            owner='Bela1',
            type='Magán'
        )
        Auto.objects.create(
            average_fuel=12.3,
            delegation_starting=0,
            delegation_ending=123,
            driver='Bela',
            owner='Bela2',
            type='Magán'
        )
        Auto.objects.create(
            average_fuel=12.3,
            delegation_starting=0,
            delegation_ending=123,
            driver='Bela',
            owner='Bela3',
            type='Magán'
        )

    def test_get_all_autos_no_auth(self):
        """
        Test module for GET all autos without authnetication
        """
        self.setup_autok()
        response = self.client.get(reverse('auto-list'))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all_autos(self):
        """
        Test module for GET all autos
        """
        self.setup_autok()
        self.client.force_authenticate(self.user)
        response = self.client.get(reverse('auto-list'))

        autok = Auto.objects.all()
        serializer = AutoSerializer(autok, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_autos_nested(self):
        self.setup_autok()
        self.client.force_authenticate(self.user)
        response = self.client.get(
            reverse('auto-list'),
            {'query': 'nested'}
        )

        autok = Auto.objects.all()
        serializer = AutoSerializer(autok, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_autos_flat(self):
        self.setup_autok()
        self.client.force_authenticate(self.user)
        response = self.client.get(
            reverse('auto-list'),
            {'query': 'notnested'}
        )

        autok = Auto.objects.all()
        serializer = AutoSerializer(autok, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AutoGetSingleTest(APITestCase):
    """
    Test module for GET a single auto
    """

    def setUp(self):
        self.user = User.objects.create_user(username="user1", email="user1@test.com", password="password1")
        self.client = APIClient()

    def setup_autok(self):
        Auto.objects.create(
            average_fuel=12.3,
            delegation_starting=0,
            delegation_ending=123,
            driver='Bela',
            owner='Bela1',
            type='Magán'
        )
        self.auto = Auto.objects.create(
            average_fuel=12.3,
            delegation_starting=0,
            delegation_ending=123,
            driver='Bela',
            owner='Bela2',
            type='Magán'
        )
        Auto.objects.create(
            average_fuel=12.3,
            delegation_starting=0,
            delegation_ending=123,
            driver='Bela',
            owner='Bela3',
            type='Magán'
        )

    def test_get_single_auto_no_auth(self):
        """
        Test module for GET a single auto without authentication
        """
        self.setup_autok()
        response = self.client.get(
            reverse('auto-detail', kwargs={'pk': self.auto.id})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_single_auto(self):
        """
        Test module for GET a single auto
        """
        self.setup_autok()
        self.client.force_authenticate(self.user)
        response = self.client.get(
            reverse('auto-detail', kwargs={'pk': self.auto.id})
        )

        serializer = AutoSerializer(self.auto)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_auto_invalid_id(self):
        """
        Test module for GET a single auto with Invalid ID
        """
        self.setup_autok()
        self.client.force_authenticate(self.user)
        response = self.client.get(
            reverse('auto-detail', kwargs={'pk': 99})
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_single_auto_nested(self):
        self.setup_autok()
        self.client.force_authenticate(self.user)
        response = self.client.get(
            reverse('auto-detail', kwargs={'pk': self.auto.id}),
            {'query': 'nested'}
        )

        serializer = AutoSerializer(self.auto)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_auto_flat(self):
        self.setup_autok()
        self.client.force_authenticate(self.user)
        response = self.client.get(
            reverse('auto-detail', kwargs={'pk': self.auto.id}),
            {'query': 'nope'}
        )

        serializer = AutoSerializer(self.auto)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AutoDeleteTest(APITestCase):
    """
    Test module for deleting an existing auto
    """

    def setUp(self):
        self.user = User.objects.create_user(username="user1", email="user1@test.com", password="password1")
        self.client = APIClient()

        self.auto = Auto.objects.create(
            average_fuel=12.3,
            delegation_starting=0,
            delegation_ending=123,
            driver='Bela',
            owner='Bela1',
            type='Magán'
        )
        Auto.objects.create(
            average_fuel=12.3,
            delegation_starting=0,
            delegation_ending=123,
            driver='Bela',
            owner='Bela2',
            type='Magán'
        )

    def test_auto_delete(self):
        self.client.force_authenticate(self.user)
        response = self.client.delete(
            reverse('auto-detail', kwargs={'pk': self.auto.id}),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Auto.objects.count(), 2)
        self.assertNotEqual(Auto.objects.first().deleted_at, None)

        # Check get a single auto
        response = self.client.delete(
            reverse('auto-detail', kwargs={'pk': self.auto.id}),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Check get list
        response = self.client.get(reverse('auto-list'))
        autok = Auto.objects.filter(deleted_at=None)
        serializer = AutoSerializer(autok, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(Auto.objects.count(), 2)

    def test_auto_delete_no_auth(self):

        response = self.client.delete(
            reverse('auto-detail', kwargs={'pk': self.auto.id}),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_auto_delete_invalid_id(self):
        self.client.force_authenticate(self.user)
        response = self.client.delete(
            reverse('auto-detail', kwargs={'pk': 99}),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AutoPartnerConnectionCreateTest(APITestCase):
    """
    Test Module for creation of AutoPartnerConnection
    """

    def setUp(self):
        self.user = User.objects.create_user(username="user1", email="user1@test.com", password="password1")
        self.client = APIClient()

        self.auto = Auto.objects.create(
            average_fuel=12.3,
            delegation_starting=0,
            delegation_ending=123,
            driver='Bela',
            owner='Bela2',
            type='Magán'
        )
        self.partner = Partner.objects.create(
            name='Bolt2',
            city='LA',
            address='4035 Cím utca 8',
            company_name='Bolt1'
        )

    def test_create_no_auth(self):
        data = {
            "partner": self.partner.id
        }
        response = self.client.post(
            reverse('auto-detail', kwargs={'pk': self.auto.id}),
            data,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_autopartner(self):
        data = {
            "partner": self.partner.id
        }
        self.client.force_authenticate(self.user)
        response = self.client.post(
            reverse('auto-detail', kwargs={'pk': self.auto.id}),
            data,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AutoPartnerConnection.objects.count(), 1)
        self.assertEqual(
            AutoPartnerConnection.objects.first().auto,
            self.auto)
        self.assertEqual(
            AutoPartnerConnection.objects.first().partner,
            self.partner
        )

    def test_create_invalid_partner_id(self):
        data = {
            "partner": 99
        }
        self.client.force_authenticate(self.user)
        response = self.client.post(
            reverse('auto-detail', kwargs={'pk': self.auto.id}),
            data,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_auto_id(self):
        data = {
            "partner": self.partner.id
        }
        self.client.force_authenticate(self.user)
        response = self.client.post(
            reverse('auto-detail', kwargs={'pk': 99}),
            data,
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AutoPartnerNestFlatTest(APITestCase):
    """
    Test module for cheking query GET parameter
    """

    def setUp(self):
        self.user = User.objects.create_user(username="user1", email="user1@test.com", password="password1")
        self.client = APIClient()

        auto1 = Auto.objects.create(
            average_fuel=12.3,
            delegation_starting=0,
            delegation_ending=123,
            driver='Bela',
            owner='Bela2',
            type='Magán'
        )
        self.auto = Auto.objects.create(
            average_fuel=12.3,
            delegation_starting=0,
            delegation_ending=123,
            driver='Bela',
            owner='Bela2',
            type='Magán'
        )
        self.partner = Partner.objects.create(
            name='Bolt2',
            city='LA',
            address='4035 Cím utca 8',
            company_name='Bolt1'
        )
        partner2 = Partner.objects.create(
            name='Bolt2',
            city='LA',
            address='4035 Cím utca 8',
            company_name='Bolt1'
        )
        AutoPartnerConnection.objects.create(
            auto=self.auto,
            partner=self.partner
        )
        AutoPartnerConnection.objects.create(
            auto=self.auto,
            partner=partner2
        )
        AutoPartnerConnection.objects.create(
            auto=auto1,
            partner=self.partner
        )

    def test_get_all_partners_nested_flat(self):
        self.client.force_authenticate(self.user)
        response_nested = self.client.get(
            reverse('partner-list'),
            {'query': 'nested'}
        )

        response = self.client.get(
            reverse('partner-list'),
            {'query': 'NOt nested'}
        )

        self.assertNotEqual(response.data, response_nested.data)

    def test_get_single_partners_nested_flat(self):
        self.client.force_authenticate(self.user)
        response_nested = self.client.get(
            reverse('partner-detail', kwargs={'pk': self.partner.id}),
            {'query': 'nested'}
        )

        response = self.client.get(
            reverse('partner-detail', kwargs={'pk': self.partner.id}),
            {'query': 'NOt nested'}
        )

        self.assertNotEqual(response.data, response_nested.data)

    def test_get_all_auto_nested_flat(self):
        self.client.force_authenticate(self.user)
        response_nested = self.client.get(
            reverse('auto-list'),
            {'query': 'nested'}
        )

        response = self.client.get(
            reverse('auto-list'),
            {'query': 'NOt nested'}
        )

        self.assertNotEqual(response.data, response_nested.data)

    def test_get_single_auto_nested_flat(self):
        self.client.force_authenticate(self.user)
        response_nested = self.client.get(
            reverse('auto-detail', kwargs={'pk': self.auto.id}),
            {'query': 'nested'}
        )

        response = self.client.get(
            reverse('auto-detail', kwargs={'pk': self.auto.id}),
            {'query': 'NOt nested'}
        )

        self.assertNotEqual(response.data, response_nested.data)


class AutoPartnerDeleteTest(APITestCase):
    """
    Test module for checking auto, partner connection deletion
    """

    def setUp(self):
        self.user = User.objects.create_user(username="user2", email="user1@test.com", password="password1")
        self.client = APIClient()

        auto1 = Auto.objects.create(
            average_fuel=12.3,
            delegation_starting=0,
            delegation_ending=123,
            driver='Bela',
            owner='Bela2',
            type='Magán'
        )
        self.auto = Auto.objects.create(
            average_fuel=12.3,
            delegation_starting=0,
            delegation_ending=123,
            driver='Bela',
            owner='Bela2',
            type='Magán'
        )
        self.partner = Partner.objects.create(
            name='Bolt2',
            city='LA',
            address='4035 Cím utca 8',
            company_name='Bolt1'
        )
        partner2 = Partner.objects.create(
            name='Bolt2',
            city='LA',
            address='4035 Cím utca 8',
            company_name='Bolt1'
        )
        AutoPartnerConnection.objects.create(
            auto=self.auto,
            partner=self.partner
        )
        AutoPartnerConnection.objects.create(
            auto=self.auto,
            partner=partner2
        )
        AutoPartnerConnection.objects.create(
            auto=auto1,
            partner=self.partner
        )

        # extra data for comparison
        self.auto_count = Auto.objects.count()
        self.partner_count = Partner.objects.count()
        response = self.client.get(reverse('auto-list'))
        self.auto_list = response.data
        response = self.client.get(reverse('partner-list'))
        self.partner_list = response.data

    def test_delete_auto(self):
        self.client.force_authenticate(self.user)
        response = self.client.delete(
            reverse('auto-detail', kwargs={'pk': self.auto.id}),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # there was no actual deletion
        self.assertEqual(Auto.objects.count(), self.auto_count)
        self.assertEqual(Partner.objects.count(), self.partner_count)
        self.assertNotEqual(
            Auto.objects.get(id=self.auto.id).deleted_at,
            None
        )

        # Check get list is shorter then original
        response = self.client.get(reverse('auto-list'))
        autok = Auto.objects.filter(deleted_at=None)
        serializer = AutoSerializer(autok, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertNotEqual(self.auto_list, response.data)

        response = self.client.get(reverse('partner-list'))
        partnerek = Partner.objects.filter(deleted_at=None)
        serializer = PartnerSerializer(partnerek, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertNotEqual(self.partner_list, response.data)

    def test_delete_partner(self):
        self.client.force_authenticate(self.user)
        response = self.client.delete(
            reverse('partner-detail', kwargs={'pk': self.partner.id}),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # there was no actual deletion
        self.assertEqual(Auto.objects.count(), self.auto_count)
        self.assertEqual(Partner.objects.count(), self.partner_count)
        self.assertNotEqual(
            Partner.objects.get(id=self.partner.id).deleted_at,
            None
        )

        # Check get list is shorter then original
        response = self.client.get(reverse('auto-list'))
        autok = Auto.objects.filter(deleted_at=None)
        serializer = AutoSerializer(autok, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertNotEqual(self.auto_list, response.data)

        response = self.client.get(reverse('partner-list'))
        partnerek = Partner.objects.filter(deleted_at=None)
        serializer = PartnerSerializer(partnerek, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertNotEqual(self.partner_list, response.data)


# class AutoPartnerConnectionGetAllTest(APITestCase):
#     """
#     Test Module for GET all AutoPartnerConnection
#     """

#     def setUp(self):
#         self.user = User.objects.create_user(username="user1", email="user1@test.com", password="password1")
#         self.client = APIClient()

#         auto1 = Auto.objects.create(
#             average_fuel=12.3,
#             delegation_starting=0,
#             delegation_ending=123,
#             driver='Bela',
#             owner='Bela2',
#             type='Magán'
#         )
#         auto2 = Auto.objects.create(
#             average_fuel=12.3,
#             delegation_starting=0,
#             delegation_ending=123,
#             driver='Bela',
#             owner='Bela2',
#             type='Magán'
#         )
#         partner1 = Partner.objects.create(
#             name='Bolt2',
#             city='LA',
#             address='4035 Cím utca 8',
#             company_name='Bolt1'
#         )
#         partner2 = Partner.objects.create(
#             name='Bolt2',
#             city='LA',
#             address='4035 Cím utca 8',
#             company_name='Bolt1'
#         )
#         AutoPartnerConnection.objects.create(
#             auto=auto1,
#             partner=partner1
#         )
#         AutoPartnerConnection.objects.create(
#             auto=auto1,
#             partner=partner2
#         )
#         AutoPartnerConnection.objects.create(
#             auto=auto2,
#             partner=partner1
#         )

#     def test_get_all_autopartner_no_auth(self):
#         response = self.client.get(reverse('kapcsolat-list'))
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     def test_get_all_autopartner(self):
#         self.client.force_authenticate(self.user)
#         response = self.client.get(reverse('kapcsolat-list'))

#         kapcsolatok = AutoPartnerConnection.objects.all()
#         serializer = AutoPartnerConnectionSerializer(kapcsolatok, many=True)
#         self.assertEqual(response.data, serializer.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


# class AutoPartnerConnectionGetSingleTest(APITestCase):
#     """
#     Test Module for GET a single AutoPartnerConnection
#     """

#     def setUp(self):
#         self.user = User.objects.create_user(username="user1", email="user1@test.com", password="password1")
#         self.client = APIClient()

#         auto1 = Auto.objects.create(
#             average_fuel=12.3,
#             delegation_starting=0,
#             delegation_ending=123,
#             driver='Bela',
#             owner='Bela2',
#             type='Magán'
#         )
#         auto2 = Auto.objects.create(
#             average_fuel=12.3,
#             delegation_starting=0,
#             delegation_ending=123,
#             driver='Bela',
#             owner='Bela2',
#             type='Magán'
#         )
#         partner1 = Partner.objects.create(
#             name='Bolt2',
#             city='LA',
#             address='4035 Cím utca 8',
#             company_name='Bolt1'
#         )
#         partner2 = Partner.objects.create(
#             name='Bolt2',
#             city='LA',
#             address='4035 Cím utca 8',
#             company_name='Bolt1'
#         )
#         AutoPartnerConnection.objects.create(
#             auto=auto1,
#             partner=partner1
#         )
#         self.kapcs = AutoPartnerConnection.objects.create(
#             auto=auto1,
#             partner=partner2
#         )
#         AutoPartnerConnection.objects.create(
#             auto=auto2,
#             partner=partner1
#         )

#     def test_get_single_autopartner_no_auth(self):
#         response = self.client.get(
#             reverse('kapcsolat-detail', kwargs={'pk': self.kapcs.id}),
#             format='json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     def test_get_single_autopartner(self):
#         self.client.force_authenticate(self.user)
#         response = self.client.get(
#             reverse('kapcsolat-detail', kwargs={'pk': self.kapcs.id}),
#             format='json'
#         )

#         serializer = AutoPartnerConnectionSerializer(self.kapcs)
#         # self.assertEqual(response.data, serializer.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


# class AutoPartnerConnectionDeleteTest(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username="user1", email="user1@test.com", password="password1")
#         self.client = APIClient()

#         auto1 = Auto.objects.create(
#             average_fuel=12.3,
#             delegation_starting=0,
#             delegation_ending=123,
#             driver='Bela',
#             owner='Bela2',
#             type='Magán'
#         )
#         auto2 = Auto.objects.create(
#             average_fuel=12.3,
#             delegation_starting=0,
#             delegation_ending=123,
#             driver='Bela',
#             owner='Bela2',
#             type='Magán'
#         )
#         partner1 = Partner.objects.create(
#             name='Bolt2',
#             city='LA',
#             address='4035 Cím utca 8',
#             company_name='Bolt1'
#         )
#         partner2 = Partner.objects.create(
#             name='Bolt2',
#             city='LA',
#             address='4035 Cím utca 8',
#             company_name='Bolt1'
#         )
#         self.kapcs = AutoPartnerConnection.objects.create(
#             auto=auto1,
#             partner=partner1
#         )
#         AutoPartnerConnection.objects.create(
#             auto=auto1,
#             partner=partner2
#         )
#         AutoPartnerConnection.objects.create(
#             auto=auto2,
#             partner=partner1
#         )

#     def test_autopartner_delete(self):
#         self.client.force_authenticate(self.user)
#         response = self.client.delete(
#             reverse('kapcsolat-detail', kwargs={'pk': self.kapcs.id}),
#             format='json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(AutoPartnerConnection.objects.count(), 3)
#         self.assertNotEqual(
#             AutoPartnerConnection.objects.first().deleted_at,
#             None
#         )

#         # Check get a single AutoPartnerConnection
#         response = self.client.delete(
#             reverse('kapcsolat-detail', kwargs={'pk': self.kapcs.id}),
#             format='json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#         # Check get list of AutoPartnerConnection
#         response = self.client.get(reverse('kapcsolat-list'))
#         kapcsolatok = AutoPartnerConnection.objects.filter(deleted_at=None)
#         serializer = AutoPartnerConnectionSerializer(kapcsolatok, many=True)
#         self.assertEqual(response.data, serializer.data)
#         self.assertEqual(Partner.objects.count(), 2)

#     def test_autopartner_delete_no_auth(self):
#         response = self.client.delete(
#             reverse('kapcsolat-detail', kwargs={'pk': self.kapcs.id}),
#             format='json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     def test_auto_delete_invalid_id(self):
#         self.client.force_authenticate(self.user)
#         response = self.client.delete(
#             reverse('kapcsolat-detail', kwargs={'pk': 99}),
#             format='json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
