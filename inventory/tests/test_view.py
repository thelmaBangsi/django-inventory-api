from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from inventory.factories import ProductFactory

class ProductAPITests(APITestCase):
    def setUp(self):
        self.product = ProductFactory(category="Electronics", stock=10)
        self.url = reverse('product-list-create')

    def test_get_product_list(self):
        """Ensure anyone can view the product list"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_filter_products_by_exact_stock(self):
        """Test exact stock filtering and ensure missing stock yields empty list"""
        response = self.client.get(f"{self.url}?stock=10")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        # Non-existent stock should return an empty list
        response_empty = self.client.get(f"{self.url}?stock=999")
        self.assertEqual(response_empty.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_empty.data), 0)

    def test_delete_product_returns_200(self):
        """Staff users can delete products with a custom 200 OK response"""
        admin_user = User.objects.create_superuser(username="admin", email="admin@admin.com", password="password")
        self.client.force_authenticate(user=admin_user)
        
        detail_url = reverse('product-detail', kwargs={'pk': self.product.id})
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)