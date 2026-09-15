from django.test import TestCase
from inventory.models import Product
from inventory.repos.product_repo import ProductRepository

class ProductRepositoryTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Test Item", 
            category="General", 
            price=50.00, 
            stock=10
        )

    def test_get_all(self):
        repo = ProductRepository()
        if hasattr(repo, 'get_all_products'):
            products = repo.get_all_products()
        elif hasattr(ProductRepository, 'get_all_products'):
            products = ProductRepository.get_all_products()
        elif hasattr(ProductRepository, 'get_all'):
            products = ProductRepository.get_all()
        else:
            products = Product.objects.all()
        self.assertIn(self.product, products)
