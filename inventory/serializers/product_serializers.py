from rest_framework import serializers
from inventory.models import Product
from django.contrib.auth.models import User
from rest_framework import serializers 


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer to convert Product data to JSON and validate incoming payloads.
    """
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'price', 'stock', 'created_at']
        read_only_fields = ['id', 'created_at']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta: 
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'), 
            password=validated_data['password']

        )
        return user 
        