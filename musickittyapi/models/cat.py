from django.db import models
from .location import Location

class Cat(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    age = models.CharField(max_length=255)
    sex = models.CharField(max_length=255)
    bio = models.TextField()
    image = models.CharField(max_length=255)  # If storing URLs. Consider ImageField if storing actual images.
    adopted = models.BooleanField()
    gets_along_with_cats = models.BooleanField()
    gets_along_with_dogs = models.BooleanField()
    gets_along_with_children = models.BooleanField()
    favorited_by = models.ManyToManyField("Profile", through='CatFavorite', related_name="favorited_cats_through")
