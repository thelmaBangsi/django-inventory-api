from django.test import TestCase 
from inventory.models import Product

class ProductModelTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Mechanical Keyboard",
            category="Electronics",
            price=89.99,
            stock=20
        )

    def test_product_creation(self): 
        """
        Ensure product is created with correct attributes
        """
        self.assertEqual(self.product.name, "Mechanical Keyboard")
        self.assertEqual(self.product.category, "Electronics")
        self.assertEqual(float(self.product.price), 89.99)
        self.assertEqual(self.product.stock, 20)

    def test_product_string_representation(self):
        """ Ensure the string representation matches expected output"""
        self.assertEqual(str(self.product), self.product.name) 