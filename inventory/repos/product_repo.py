from inventory.models import Product

class ProductRepository:
    @staticmethod
    def get_all():
        return Product.objects.all()

    @staticmethod
    def get_by_id(product_id):
        return Product.objects.filter(id=product_id).first()

    @staticmethod
    def create(data):
        return Product.objects.create(**data)
