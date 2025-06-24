from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('researcher', 'Researcher'),
        ('admin', 'Administrator'),
        ('viewer', 'Viewer'),
    ]

    # Override username to make it non-unique
    username = models.CharField(max_length=150, unique=False)
    email = models.EmailField(unique=True)  # Use email for login
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='viewer')
    is_active = models.BooleanField(default=False)  # For email verification

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Required when creating a user via createsuperuser

    def __str__(self):
        return self.email
