# models/profile_adoptions.py
from django.db import models
from .profile import Profile
from .cat import Cat

class ProfileAdoption(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)
    adoption_date = models.DateField()
    status = models.CharField(max_length=255)
