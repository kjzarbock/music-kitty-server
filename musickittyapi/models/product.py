from django.db import models
from .location import Location  

class Product(models.Model):
    description = models.TextField()
    price = models.FloatField()
    image = models.CharField(max_length=255)
    locations = models.ManyToManyField(Location)
