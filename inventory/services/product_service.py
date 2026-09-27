<<<<<<< HEAD
<<<<<<< HEAD
from inventory.repos.product_repo import ProductRepository

class ProductService:
    """"
    Handles business logic and rules for products.
    Acts as the middleman between API views and the Repository layers.
    """

    @staticmethod
    def list_all_products():
        #business logic can later go here (e.g., logging, filtering rules)
        return ProductRepository.get_all_products()

    @staticmethod
    def get_product_by_id(product_id):
        product = ProductRepository.get_product_by_id(product_id)
        if not product:
            raise ValueError(f"Product with ID {product_ID} does not exist.")
        return product

    @staticmethod 
    def register_product(validated_data): 
        #business rule example: ensuring price isn't negative before saving 
        if validated_data.get('price', 0) < 0:
            raise ValueError("Product price cannot be negative.")


        return ProductRepository.create_product(validated_data)
    
=======
=======
>>>>>>> fc9e15cac64e90c9743f8920246eede0efd88882
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
<<<<<<< HEAD
>>>>>>> fc9e15cac64e90c9743f8920246eede0efd88882
=======
>>>>>>> fc9e15cac64e90c9743f8920246eede0efd88882
