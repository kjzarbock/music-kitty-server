from django.db import models

class CatFavorite(models.Model):
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="favorite_relationships")
    cat = models.ForeignKey("Cat", on_delete=models.CASCADE, related_name="favorited_by_profiles")
