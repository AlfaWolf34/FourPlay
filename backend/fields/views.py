from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from .models import Field
from .serializers import FieldSerializer

class FieldViewSet(ModelViewSet):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer
