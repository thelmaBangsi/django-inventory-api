from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    @property
    def total_price(self): 
        return self.quantity * self.price
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

