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
    