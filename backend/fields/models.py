from django.db import models

# Create your models here.
class Field(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    price_per_hour = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.URLField(blank=True)
    description = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
