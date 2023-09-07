from django.db import models

class Cat(models.Model):
    location = models.ForeignKey('Locations', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    age = models.CharField(max_length=255)
    sex = models.CharField(max_length=10)
    bio = models.CharField(max_length=1000)
    image = models.CharField(max_length=255)
    adopted = models.BooleanField(default=False)
    gets_along_with_cats = models.BooleanField(default=False)
    gets_along_with_dogs = models.BooleanField(default=False)
    gets_along_with_children = models.BooleanField(default=False)