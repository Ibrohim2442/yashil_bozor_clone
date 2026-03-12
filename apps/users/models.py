from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.products.models import Product
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
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        blank=True,
        null=True
    )
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def phone(self):
        return self.user.phone

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.user.phone})"

class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorites"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="favorites"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # unique_together = ('user', 'product')
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'product'),
                name='to check user have unique product in favorite',
                violation_error_message="You already added this product to favorites."
            )
        ]

    def __str__(self):
        return f"{self.user} → {self.product}"