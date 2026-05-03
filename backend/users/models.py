from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True)
    is_player = models.BooleanField(default=True)

    ROLE_CHOICES = [
        (1, 'Admin'),
        (2, 'Owner'),
        (3, 'User'),
    ]

    role = models.IntegerField(choices=ROLE_CHOICES, default=3)

# Create your models here.
