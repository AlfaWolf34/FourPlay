from django.db import models
from django.conf import settings
from fields.models import Field

User = settings.AUTH_USER_MODEL


class Booking(models.Model):

    STATUS_PENDING = 'pending'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_CANCELLED = 'cancelled'
    STATUS_PAYMENT_FAILED = 'payment_failed'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pendiente de pago'),
        (STATUS_CONFIRMED, 'Confirmada'),
        (STATUS_CANCELLED, 'Cancelada'),
        (STATUS_PAYMENT_FAILED, 'Pago fallido'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='bookings')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date', 'start_time']

    def __str__(self):
        return f"{self.field.name} | {self.date} {self.start_time}-{self.end_time} | {self.get_status_display()}"