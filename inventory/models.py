from django.db import models
#this line is importing Django's object relational Mapper (ORM). 
#this tool lets me write python instead of raw sql queries like create table to talk to the db

class Product(models.Model): #below is the blueprint for product that is being turned into a table. 
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

#every attibute defined inside the model class becomes a column in that db table
#hence writing model.---correctly maps out the sl db s



    def __str__(self): 
        return self.name 
    #the above two lines allows the actual name of the product to be displayed. 
    #instead of a code technical name such as Product Object (1)
