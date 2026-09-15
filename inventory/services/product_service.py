from decimal import Decimal, InvalidOperation
from django.shortcuts import get_object_or_404
from inventory.models import Product

class ProductService:
    @staticmethod
    def list_products():
        return Product.objects.all()

    @staticmethod
    def get_product_by_id(pk):
        return get_object_or_404(Product, pk=pk)

    @staticmethod
    def create_product(data):
        raw_price = data.get('price', 0)
        try:
            price = Decimal(str(raw_price))
        except (InvalidOperation, TypeError, ValueError):
            raise ValueError("Invalid price value.")

        if price <= 0:
            raise ValueError("Price must be greater than zero.")

        return Product.objects.create(
            name=data.get('name'),
            category=data.get('category'),
            price=price,
            stock=data.get('stock', 0)
        )

    @staticmethod
    def update_product(pk, data):
        product = get_object_or_404(Product, pk=pk)
        
        if 'price' in data:
            try:
                price = Decimal(str(data['price']))
            except (InvalidOperation, TypeError, ValueError):
                raise ValueError("Invalid price value.")

            if price <= 0:
                raise ValueError("Price must be greater than zero.")
            product.price = price

        product.name = data.get('name', product.name)
        product.category = data.get('category', product.category)
        product.stock = data.get('stock', product.stock)
        product.save()
        return product

    @staticmethod
    def delete_product(pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
