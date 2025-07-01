from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point

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
    coordinates = models.PointField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_deals = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} - {self.get_user_type_display()}"

    def save(self, *args, **kwargs):
        if self.location and not self.coordinates:
            # محاكاة تحويل العنوان إلى إحداثيات
            lat, lng = self.geocode_location(self.location)
            if lat and lng:
                self.coordinates = Point(lng, lat)
        super().save(*args, **kwargs)

    def geocode_location(self, location):
        # محاكاة geocoding - في الإنتاج استخدم Google Maps API
        locations_map = {
            'القاهرة': (30.0444, 31.2357),
            'الجيزة': (30.0131, 31.2089),
            'الإسكندرية': (31.2001, 29.9187),
            'الدقهلية': (31.0409, 31.3785),
            'الشرقية': (30.5965, 31.5041),
        }
        return locations_map.get(location, (None, None))
