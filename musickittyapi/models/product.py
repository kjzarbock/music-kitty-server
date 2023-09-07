from django.db import models

class Product(models.Model):
    description = models.TextField()
    price = models.FloatField()
    image = models.CharField(max_length=255)
    location = models.ForeignKey('Locations', on_delete=models.CASCADE)