from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAdminUser
from .models import Field
from .serializers import FieldSerializer


class FieldViewSet(ModelViewSet):
    queryset = Field.objects.filter(is_available=True)
    serializer_class = FieldSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [AllowAny()]
        return [IsAdminUser()]