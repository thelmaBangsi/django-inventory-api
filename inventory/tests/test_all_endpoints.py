from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from inventory.models import Product
from inventory.factories import ProductFactory

class AllEndpointsAPITestCase(APITestCase):
    def setUp(self):
        # Create users for auth permission testing
        self.regular_user = User.objects.create_user(username="RegularGuy", email="reg@gmail.com", password="password123")
        self.admin_user = User.objects.create_superuser(username="AdminBoss", email="admin@gmail.com", password="password123")
        
        # Create test product via factory
        self.product = ProductFactory(name="Wireless Mouse", category="Accessories", price=25.50, stock=10)
        
        # URL mappings
        self.list_url = reverse('product-list-create')
        self.detail_url = reverse('product-detail', kwargs={'pk': self.product.id})
        self.register_url = reverse('register')
        self.token_url = reverse('token_obtain_pair')

    def test_1_get_product_list_endpoint(self):
        """GET /api/products/ - Publicly accessible list view"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_2_post_product_create_endpoint_permissions(self):
        """POST /api/products/ - Enforces IsAdminOrReadOnly permissions"""
        data = {"name": "Mechanical Keyboard", "category": "Peripherals", "price": 75.00, "stock": 15}
        
        # Unauthenticated / regular user should be blocked
        response = self.client.post(self.list_url, data)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

        # Admin user should successfully create product
        self.client.force_authenticate(user=self.admin_user)
        response_admin = self.client.post(self.list_url, data)
        self.assertEqual(response_admin.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_admin.data['name'], "Mechanical Keyboard")

    def test_3_get_product_detail_endpoint(self):
        """GET /api/products/{id}/ - Retrieve single product details"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product.name)

    def test_4_put_product_update_endpoint(self):
        """PUT /api/products/{id}/ - Full update by admin"""
        self.client.force_authenticate(user=self.admin_user)
        data = {"name": "Updated Mouse", "category": "Accessories", "price": 30.00, "stock": 8}
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Updated Mouse")

    def test_5_delete_product_endpoint(self):
        """DELETE /api/products/{id}/ - Custom 200 OK deletion response for admin"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Product deleted successfully")

    def test_6_product_filtering_endpoints(self):
        """Test all query parameter filters (category, stock, min_stock)"""
        # Category filter
        res_cat = self.client.get(f"{self.list_url}?category=Accessories")
        self.assertEqual(res_cat.status_code, status.HTTP_200_OK)
        
        # Exact stock filter match
        res_stock = self.client.get(f"{self.list_url}?stock=10")
        self.assertEqual(res_stock.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_stock.data), 1)

        # Exact stock filter non-existent (should return empty list [])
        res_empty = self.client.get(f"{self.list_url}?stock=9999")
        self.assertEqual(res_empty.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_empty.data), 0)

        # Minimum stock threshold filter
        res_min = self.client.get(f"{self.list_url}?min_stock=5")
        self.assertEqual(res_min.status_code, status.HTTP_200_OK)

    def test_7_user_registration_endpoint(self):
        """POST /api/register/ - User account creation with strict validation"""
        data = {
            "username": "BrandNewUser1",
            "email": "brandnew@gmail.com",
            "password": "securepassword123"
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_8_jwt_token_obtain_endpoint(self):
        """POST /api/token/ - JWT login generation"""
        data = {
            "username": "RegularGuy",
            "password": "password123"
        }
        response = self.client.post(self.token_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)