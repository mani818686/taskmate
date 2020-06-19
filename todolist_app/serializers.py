from rest_framework import serializers
from .models import tasklist
class todolistSerializer(serializers.ModelSerializer):
    class Meta:
        model = tasklist
        fields = '__all__'