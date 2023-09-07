from django.db import models

class AdopterAdoption(models.Model):
    adopter = models.ForeignKey('Adopter', on_delete=models.CASCADE)
    cat = models.ForeignKey('Cats', on_delete=models.CASCADE)
    adoption_date = models.DateField()
    status = models.CharField(max_length=255)