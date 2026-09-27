from django.test import TestCase
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