from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPES = [
        ('individual', 'فرد'),
        ('workshop', 'ورشة تدوير'),
        ('collector', 'جامع خردة'),
        ('organization', 'جمعية بيئية'),
        ('company', 'شركة'),
        ('admin', 'مدير'),
    ]
    
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='individual')
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    organization = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_deals = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} - "
