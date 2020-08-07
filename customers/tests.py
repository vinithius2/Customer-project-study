# Django Imports
from django.urls import reverse

# Third Party Imports
from rest_framework.status import HTTP_405_METHOD_NOT_ALLOWED
from rest_framework.test import APITestCase
from model_bakery import baker

# Project Imports
from customers.serializer import CustomerSerializer


class CustomerViewSetTest(APITestCase):
    def setUp(self):
        self.city_01 = baker.make('customers.City', name="Fortaleza CE")
        self.city_02 = baker.make('customers.City', name="Aquiraz CE")
        self.customer_01 = baker.make(
            'customers.Customer',
            pk=1,
            city=self.city_01,
            _fill_optional=True
        )
        self.customer_02 = baker.make(
            'customers.Customer',
            pk=2,
            city=self.city_02,
            _fill_optional=True
        )
        self.customer_03 = baker.make(
            'customers.Customer',
            pk=3,
            city=self.city_02,
            _fill_optional=True
        )

    def test_customer_get_list(self):
        url = reverse('customer:customer-list')
        resp = self.client.get(url)
        self.assertEqual(len(resp.data), 3)

    def test_customer_get_detail(self):
        url = reverse('customer:customer-detail', kwargs={'pk': self.customer_01.pk})
        serializer = CustomerSerializer(self.customer_01)
        resp = self.client.get(url)
        self.assertDictEqual(resp.data, serializer.data)

    def test_customer_delete(self):
        url = reverse('customer:customer-detail', kwargs={'pk': self.customer_01.pk})
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, HTTP_405_METHOD_NOT_ALLOWED)

    def test_customer_post(self):
        url = reverse('customer:customer-list')
        customer = baker.prepare('customers.Customer', _fill_optional=True)
        serializer = CustomerSerializer(customer)
        data = dict(serializer.data)
        del data['pk']
        resp = self.client.post(url, data=data, format='json')
        self.assertEqual(resp.status_code, HTTP_405_METHOD_NOT_ALLOWED)

    def test_customer_put(self):
        url = reverse('customer:customer-detail', kwargs={'pk': self.customer_01.pk})
        self.customer_01.first_name = "Change first name..."
        serializer = CustomerSerializer(self.customer_01)
        resp = self.client.put(url, data=serializer.data, format='json')
        self.assertEqual(resp.status_code, HTTP_405_METHOD_NOT_ALLOWED)

    def test_customer_patch(self):
        url = reverse('customer:customer-detail', kwargs={'pk': self.customer_01.pk})
        resp = self.client.patch(url, data={"first_name": "Change first name..."})
        self.assertEqual(resp.status_code, HTTP_405_METHOD_NOT_ALLOWED)


class CityModelTest(APITestCase):
    def setUp(self):
        self.city_01 = baker.make('customers.City', name="Fortaleza CE")

    def test_get_latitude(self):
        self.assertIsNotNone(self.city_01.latitude)

    def test_get_longitude(self):
        self.assertIsNotNone(self.city_01.longitude)
