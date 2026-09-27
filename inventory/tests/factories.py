import factory
from factory.django import DjangoModelFactory
from inventory.models import Product

class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker('word')
    category = factory.Faker('word')
    price = factory.Faker('pydecimal', left_digits=3, right_digits=2, positive=True)
    stock = factory.Faker('random_int', min=1, max=100)
