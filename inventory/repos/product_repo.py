from inventory.models import Product
<<<<<<< HEAD
#this imports the django model class earlier created to enable the ORM db
#operations within the repository scope.
class ProductRepository: 
    """"
    Handles all direct database queries for the Product model. 
    Isolates data-fetching logic away from the API views. 
    """


    @staticmethod 
    def get_all_products():
        return Product.objects.all()

    @staticmethod 
    def get_product_by_id(product_id):
        try: 
            return Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return None
    @staticmethod
    def create_product(validated_data):
        return Product.objects.create(**validated_data)
    #validated data in this case is a dictionary and ** infront of a dictionary is performing dictionary unpacking.
# without it, the code will look like 
# Product.objects.create(
#     name=validated_data['name'], 
#     price=validated data['price']
#     stock=validated data['stock']
#     category=validated data['category']
#     and so on for every field....
#)    
=======

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
>>>>>>> fc9e15cac64e90c9743f8920246eede0efd88882
