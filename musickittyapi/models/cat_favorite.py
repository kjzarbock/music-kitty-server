from django.db import models
from .profile import Profile
from .cat import Cat

class CatFavorite(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)
