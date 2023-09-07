from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    opening_hours = models.TimeField()
    closing_hours = models.TimeField()