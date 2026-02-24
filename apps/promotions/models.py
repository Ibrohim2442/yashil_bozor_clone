from django.db import models
from django.utils import timezone


# Create your models here.

class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percent = models.PositiveIntegerField()
    expire_date = models.DateTimeField()
    max_usage = models.PositiveIntegerField()
    used_count = models.PositiveIntegerField(default=0)

    def is_valid(self):
        return (
            self.used_count < self.max_usage and
            self.expire_date > timezone.now()
        )