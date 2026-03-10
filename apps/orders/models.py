from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from apps.products.models import Product


# Create your models here.

class Order(models.Model):

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("processing", "Processing"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    recipient_name = models.CharField(max_length=255)
    recipient_phone = models.CharField(max_length=20)

    courier_note = models.TextField(blank=True)

    address = models.CharField(max_length=255)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        if self.latitude is None or self.longitude is None:
            from geopy.geocoders import Nominatim

            geolocator = Nominatim(user_agent="apps")
            location = geolocator.geocode(self.address)

            if location is not None:
                print(location.longitude, location.latitude)
                print(location.raw)

                self.latitude = location.latitude
                self.longitude = location.longitude

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.id} - {self.user}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_items")
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    price = models.DecimalField(max_digits=12, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

class OrderItemReview(models.Model):
    order_item = models.OneToOneField(
        OrderItem,
        on_delete=models.CASCADE,
        related_name="review"
    )

    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    pros = models.TextField(blank=True)
    cons = models.TextField(blank=True)
    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_item.product.name