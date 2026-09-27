from django.test import TestCase
from inventory.models import Product 

class ProductServiceTests(TestCase):
    def test_product_data_layer_handling(self):
        """ 
        Test business logic and transaction handles
        """
        product = Product.objects.create(
            name="Gaming Monitor", 
            category="Displays", 
            price=299.99, 
            stock=5 
        )
        self.assertIsNotNone(product.id)
        self.assertEqual(product.category, "Displays")
        self.assertEqual(product.stock, 5)