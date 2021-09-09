"""Users models."""

# Django
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """Profile model.
    Model One to One with User model.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    address = models.CharField(max_length=100, null=True)
    town = models.CharField(max_length=100, null=True)
    county = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=60, null=True)
    post_code = models.CharField(max_length=100, null=True)

    longitude = models.CharField(max_length=50, null=True)
    latitude = models.CharField(max_length=50, null=True)

    captcha_score = models.FloatField(default=0.0)
    has_profile = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user}'
