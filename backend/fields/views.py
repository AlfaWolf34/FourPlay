from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .models import Field
from .serializers import FieldSerializer


class FieldViewSet(ModelViewSet):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer

    # Permisos
    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [AllowAny()]

        return [IsAuthenticated()]

    #FILTRO POR ROL
    def get_queryset(self):
        user = self.request.user

        #Admin → ve todo
        if user.is_authenticated and user.role == 1:
            return Field.objects.all()

        #Owner → solo sus canchas
        if user.is_authenticated and user.role == 2:
            return Field.objects.filter(owner=user)

        #Usuario normal → solo disponibles
        return Field.objects.filter(is_available=True)

    # AUTO ASIGNAR OWNER
    def perform_create(self, serializer):
        if self.request.user.role not in [1, 2]:
            raise PermissionDenied("No puedes crear canchas")

        serializer.save(owner=self.request.user)

    # PROTEGER UPDATE
    def perform_update(self, serializer):
        field = self.get_object()

        # Owner solo puede editar lo suyo
        if self.request.user.role == 2 and field.owner != self.request.user:
            raise PermissionDenied("No puedes editar esta cancha")

        # Usuario normal no puede editar
        if self.request.user.role == 3:
            raise PermissionDenied("No tienes permisos")

        serializer.save()

    # PROTEGER DELETE
    def perform_destroy(self, instance):
        # Owner solo elimina lo suyo
        if self.request.user.role == 2 and instance.owner != self.request.user:
            raise PermissionDenied("No puedes eliminar esta cancha")

        # Usuario normal no puede eliminar
        if self.request.user.role == 3:
            raise PermissionDenied("No tienes permisos")

        instance.delete()