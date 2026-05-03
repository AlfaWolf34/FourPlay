from rest_framework import serializers
from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    field_name = serializers.CharField(source='field.name', read_only=True)
    field_price = serializers.DecimalField(
        source='field.price_per_hour',
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['user', 'status', 'created_at', 'updated_at']

    # ── Validaciones individuales ─────────────────────────────────────────

    def validate(self, data):
        """Valida horario lógico, horario de operación y empalmes."""
        field = data.get('field') or getattr(self.instance, 'field', None)
        date = data.get('date') or getattr(self.instance, 'date', None)
        start_time = data.get('start_time') or getattr(self.instance, 'start_time', None)
        end_time = data.get('end_time') or getattr(self.instance, 'end_time', None)

        # 1. La hora de inicio debe ser anterior a la de fin
        if start_time and end_time and start_time >= end_time:
            raise serializers.ValidationError(
                "La hora de inicio debe ser anterior a la hora de fin."
            )

        # 2. El horario debe estar dentro del horario de operación de la cancha
        if field and start_time and end_time:
            if start_time < field.open_time or end_time > field.close_time:
                raise serializers.ValidationError(
                    f"El horario solicitado está fuera del horario de operación "
                    f"({field.open_time.strftime('%H:%M')} - {field.close_time.strftime('%H:%M')})."
                )

        # 3. Validación de empalmes con reservaciones confirmadas (RF-012)
        if field and date and start_time and end_time:
            booking_id = self.instance.id if self.instance else None
            overlap = Booking.objects.filter(
                field=field,
                date=date,
                status__in=[Booking.STATUS_PENDING, Booking.STATUS_CONFIRMED],
                start_time__lt=end_time,
                end_time__gt=start_time,
            ).exclude(id=booking_id)

            if overlap.exists():
                raise serializers.ValidationError(
                    "Ya existe una reservación que se empalma con el horario solicitado."
                )

        return data

    def create(self, validated_data):
        """Asigna automáticamente el usuario autenticado al crear."""
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user
        validated_data['status'] = Booking.STATUS_PENDING
        return super().create(validated_data)