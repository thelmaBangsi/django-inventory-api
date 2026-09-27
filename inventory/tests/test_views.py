import factory
from factory.django import DjangoModelFactory
from faker import Faker
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from inventory.models import Product

fake = Faker()

class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.LazyAttribute(lambda _: fake.word().capitalize() + " Product")
    category = factory.LazyAttribute(lambda _: fake.word().capitalize())
    price = factory.LazyAttribute(lambda _: round(fake.pyfloat(left_digits=3, right_digits=2, positive=True, min_value=1.0), 2))
    stock = factory.LazyAttribute(lambda _: fake.random_int(min=0, max=100))

class ProductAPITestCase(APITestCase):
    def setUp(self):
        self.list_create_url = reverse('product-list-create')

    def test_create_product_success(self):
        payload = {
            "name": "Wireless Mouse",
            "category": "Electronics",
            "price": "29.99",
            "stock": 15
        }
        response = self.client.post(self.list_create_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_product_invalid_price_fails(self):
        payload = {
            "name": "Invalid Item",
            "category": "Electronics",
            "price": "-5.00",
            "stock": 10
        }
        response = self.client.post(self.list_create_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('price', response.data)

    def test_list_products_pagination(self):
        ProductFactory.create_batch(7)
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 5)

    def test_filter_search_and_sort(self):
        ProductFactory.create(name="Gaming Laptop", category="Electronics", price=1200.00)
        ProductFactory.create(name="Office Desk", category="Furniture", price=250.00)

        # Test Search
        response = self.client.get(f"{self.list_create_url}?search=Laptop")
        self.assertEqual(len(response.data['results']), 1)

        # Test Filter
        response = self.client.get(f"{self.list_create_url}?category=Furniture")
        self.assertEqual(len(response.data['results']), 1)

        # Test Ordering
        response = self.client.get(f"{self.list_create_url}?ordering=-price")
        self.assertGreater(float(response.data['results'][0]['price']), float(response.data['results'][1]['price']))

    def test_update_product(self):
        product = ProductFactory.create()
        url = reverse('product-detail', kwargs={'pk': product.pk})
        payload = {"name": "Updated Laptop", "category": product.category, "price": "899.99", "stock": 5}
        response = self.client.put(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_product(self):
        product = ProductFactory.create()
        url = reverse('product-detail', kwargs={'pk': product.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
