from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    image = models.CharField(max_length=255, blank=True)  # Assuming you're storing image URLs or filenames
    bio = models.CharField(max_length=255, blank=True)
    has_cats = models.BooleanField(default=False)
    has_dogs = models.BooleanField(default=False)
    has_children = models.BooleanField(default=False)
    approved_to_adopt = models.BooleanField(default=False)


