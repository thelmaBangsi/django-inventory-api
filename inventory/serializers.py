from rest_framework import serializers
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'quantity', 'price', 'total_price', 'created_at']
