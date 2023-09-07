from django.db import models

class Reservation(models.Model):
    adopter = models.ForeignKey('Adopter', on_delete=models.CASCADE)
    location = models.ForeignKey('Locations', on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    number_of_guests = models.IntegerField()