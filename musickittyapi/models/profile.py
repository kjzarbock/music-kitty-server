from django.db import models
from django.contrib.auth.models import User
from .cat import Cat

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    image = models.CharField(max_length=255, blank=True) 
    bio = models.CharField(max_length=255, blank=True)
    has_cats = models.BooleanField(default=False)
    has_dogs = models.BooleanField(default=False)
    has_children = models.BooleanField(default=False)
    approved_to_adopt = models.BooleanField(default=False)
    favorited_cats = models.ManyToManyField(Cat, through='CatFavorite')

    @property
    def is_staff_profile(self):
        return self.user.is_staff

