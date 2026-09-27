import factory
from faker import Faker
from inventory.models import Product

fake = Faker()

class ProductFactory(factory.django.DjangoModelFactory):
    """
    Factory to generate fake Product instances for testing.
    """
    class Meta:
        model = Product

    name = factory.LazyAttribute(lambda _: fake.catch_phrase())
    category = factory.LazyAttribute(lambda _: fake.word())
    price = factory.LazyAttribute(lambda _: round(fake.random_number(digits=3, fix_len=True) + 9.99, 2))
    stock = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=100))