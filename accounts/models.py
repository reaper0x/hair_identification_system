from django.contrib.auth.models import AbstractUser
from django.db import models

is_active = models.BooleanField(default=False)

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('researcher', 'Researcher'),
        ('admin', 'Administrator'),
        ('viewer', 'Viewer'),
    ]
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
