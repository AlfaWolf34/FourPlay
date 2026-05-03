from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        if self.action == 'me':
            return [IsAuthenticated()]
        if self.action == 'set_role': 
            return [IsAuthenticated()]
        return [IsAdminUser()]

    @action(detail=False, methods=['get', 'put', 'patch'], url_path='me')
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='set_role')
    def set_role(self, request, pk=None):

        # 🔒 solo admin puede cambiar roles
        if request.user.role != 1:
            return Response(
                {'error': 'No tienes permiso'},
                status=status.HTTP_403_FORBIDDEN
            )

        user = self.get_object()
        new_role = request.data.get('role')

        # validar rol
        if new_role not in [1, 2, 3]:
            return Response(
                {'error': 'Rol inválido'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.role = new_role
        user.save()

        return Response({
            'message': 'Rol actualizado',
            'user_id': user.id,
            'new_role': user.role
        })