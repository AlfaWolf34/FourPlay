from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Booking
from .serializers import BookingSerializer


class BookingViewSet(ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(user=user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    @action(
        detail=False,
        methods=['get'],
        url_path='availability',
        permission_classes=[AllowAny]
    )
    def availability(self, request):
        """
        GET /api/bookings/availability/?field=1&date=2026-03-15
        Devuelve los slots ocupados para una cancha y fecha específicas.
        Es público para que cualquier usuario (sin login) también pueda ver disponibilidad.
        """
        field_id = request.query_params.get('field')
        date     = request.query_params.get('date')

        if not field_id or not date:
            return Response(
                {'detail': 'Se requieren los parámetros field y date.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        occupied = Booking.objects.filter(
            field_id=field_id,
            date=date,
            status__in=[Booking.STATUS_PENDING, Booking.STATUS_CONFIRMED]
        ).values('start_time', 'end_time')

        # Devuelve lista de slots ocupados en formato HH:MM
        slots = [
            {
                'start_time': b['start_time'].strftime('%H:%M'),
                'end_time':   b['end_time'].strftime('%H:%M'),
            }
            for b in occupied
        ]

        return Response({'occupied_slots': slots})

    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel(self, request, pk=None):
        """
        POST /api/bookings/{id}/cancel/
        Permite al usuario cancelar su propia reservación (RF-016).
        """
        booking = self.get_object()

        if booking.status == Booking.STATUS_CANCELLED:
            return Response(
                {'detail': 'Esta reservación ya está cancelada.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if booking.status not in [Booking.STATUS_PENDING, Booking.STATUS_CONFIRMED]:
            return Response(
                {'detail': 'Solo se pueden cancelar reservaciones pendientes o confirmadas.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        booking.status = Booking.STATUS_CANCELLED
        booking.save()
        serializer = self.get_serializer(booking)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='confirm')
    def confirm(self, request, pk=None):
        """
        POST /api/bookings/{id}/confirm/
        Simula la confirmación de pago (RF-013).
        """
        booking = self.get_object()

        if booking.status != Booking.STATUS_PENDING:
            return Response(
                {'detail': 'Solo se pueden confirmar reservaciones en estado pendiente.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        booking.status = Booking.STATUS_CONFIRMED
        booking.save()
        serializer = self.get_serializer(booking)
        return Response(serializer.data)