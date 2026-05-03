from django.db import models
from django.conf import settings

class Field(models.Model):

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='fields'
    )

    SPORT_CHOICES = [
        ('football', 'Fútbol'),
        ('basketball', 'Basquetbol'),
        ('tennis', 'Tenis'),
        ('volleyball', 'Voleibol'),
        ('other', 'Otro'),
    ]

    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    sport_type = models.CharField(
        max_length=20,
        choices=SPORT_CHOICES,
        default='football'
    )
    price_per_hour = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='fields/', null=True, blank=True)
    description = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)

    open_time = models.TimeField(help_text='Hora de apertura, ej. 08:00')
    close_time = models.TimeField(help_text='Hora de cierre, ej. 22:00')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name