from django.db import models

class CatFavorite(models.Model):
    adopter = models.ForeignKey('Adopter', on_delete=models.CASCADE)
    cat = models.ForeignKey('Cats', on_delete=models.CASCADE)