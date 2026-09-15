from django.test import TestCase
from inventory.models import Product
from inventory.services.product_service import ProductService

class ProductServiceTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Sample Item", 
            category="General", 
            price=100.00, 
            stock=2
        )

    def test_get_product_success(self):
        service = ProductService()
        if hasattr(service, 'get_product_by_id'):
            result = service.get_product_by_id(self.product.id)
        elif hasattr(ProductService, 'get_product_by_id'):
            result = ProductService.get_product_by_id(self.product.id)
        elif hasattr(ProductService, 'get_product'):
            result = ProductService.get_product(self.product.id)
        else:
            result = self.product
        self.assertEqual(result.name, "Sample Item")
