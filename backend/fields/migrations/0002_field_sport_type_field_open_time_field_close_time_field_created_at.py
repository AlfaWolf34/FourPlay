from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('fields', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='field',
            name='sport_type',
            field=models.CharField(
                choices=[
                    ('football', 'Fútbol'),
                    ('basketball', 'Basquetbol'),
                    ('tennis', 'Tenis'),
                    ('volleyball', 'Voleibol'),
                    ('other', 'Otro'),
                ],
                default='football',
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='field',
            name='open_time',
            field=models.TimeField(
                default='08:00',
                help_text='Hora de apertura, ej. 08:00',
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='field',
            name='close_time',
            field=models.TimeField(
                default='22:00',
                help_text='Hora de cierre, ej. 22:00',
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='field',
            name='created_at',
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
            ),
            preserve_default=False,
        ),
    ]
