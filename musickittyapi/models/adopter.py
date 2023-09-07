from django.db import models
from django.contrib.auth.models import User

class Adopter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='adopter')
    has_cats = models.BooleanField()
    has_dogs = models.BooleanField()
    has_children = models.BooleanField()
    approved_to_adopt = models.BooleanField()
