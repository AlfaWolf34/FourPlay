from django.db import models

# Create your models here.
from django.conf import settings
from fields.models import Field

User = settings.AUTH_USER_MODEL

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)

    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.field} - {self.date}"