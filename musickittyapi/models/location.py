from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    opening_hours = models.CharField(max_length=255)
    closing_hours = models.CharField(max_length=255)
