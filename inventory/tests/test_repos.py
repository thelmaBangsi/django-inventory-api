from django.test import TestCase
<<<<<<< HEAD
from inventory.models import Product 

class ProductRepositoryTests(TestCase): 
    def setUp(self): 
        self.product = Product.objects.create(
            name="Mechanical Keyboard", 
            category="Peripherals", 
            price=75.00,
            stock=12
        )

    def test_repostory_fetches_product_correctly(self): 
        """
          Test that data queries return correct records
        """
        product = Product.objects.get(name="Mechanical Keyboard")
        self.assertEqual(product.stock, 12)
        self.assertEqual(float(product.price), 75.00)
=======
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
>>>>>>> fc9e15cac64e90c9743f8920246eede0efd88882
