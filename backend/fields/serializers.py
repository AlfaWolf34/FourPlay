from rest_framework import serializers
from .models import Field

class FieldSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    class Meta:
        model = Field
        fields = '__all__'