from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Item

# 1. Existing Item Serializer
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'quantity', 'price', 'total_price', 'created_at']
        read_only_fields = ['id', 'total_price', 'created_at']

# 2. Registration Serializer
from rest_framework import serializers
from django.contrib.auth.models import User

# Keep your existing serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff']

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

# UPDATE OR REPLACE ONLY THIS REGISTER SERIALIZER BLOCK:
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("An account with this email address already exists.")
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

# 3. Profile Update Serializer
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        read_only_fields = ['username']

# 4. Change Password Serializer
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=6)

# 5. Forgot Password Reset Serializer
class PasswordResetRequestSerializer(serializers.Serializer):
    username_or_email = serializers.CharField(required=True)
