from django.db import models
from .profile import Profile
from .location import Location

class Reservation(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    number_of_guests = models.IntegerField()
