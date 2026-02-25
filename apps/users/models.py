from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from geopy import Nominatim
from geopy.exc import GeocoderTimedOut

from apps.users.managers import CustomUserManager


# Create your models here.

class User(AbstractUser):
    username = None
    email = None

    phone = models.CharField(max_length=20, unique=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.phone

class Address(models.Model):
    city = models.CharField(max_length=100)
    address_line = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.city}, {self.address_line}"

    def save(self, *args, **kwargs):
        if self.latitude is None or self.longitude is None:
            try:
                geolocator = Nominatim(user_agent="users")
                location = geolocator.geocode(f"{self.address_line}, {self.city}")
                if location:
                    self.latitude = location.latitude
                    self.longitude = location.longitude
            except GeocoderTimedOut:
                pass
        super().save(*args, **kwargs)

class UserProfile(models.Model):
    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    email = models.EmailField(blank=True)
    addresses = models.ManyToManyField(Address, blank=True, related_name="profiles")

    @property
    def phone(self):
        return self.user.phone

    def __str__(self):
        return f"{self.first_name} {self.last_name}"