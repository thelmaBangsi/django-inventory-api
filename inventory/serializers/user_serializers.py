import re 
from rest_framework import serializers
from django.contrib.auth.models import User 

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, allow_blank=False)

    class Meta: 
        model = User 
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True, 'allow_blank': False}

        }

    def validate_username(self, value):
        if not re.match(r'^[a-zA-Z0-9@]+$', value):
            raise serializers.ValidationError(
                "Username cannot contain negative numbers or special symbols (only letters, numbers, and '@' are allowed)"
            )

        if value.isdigit(): 
            raise serializers.ValidationError(
                "Username cannot consist solely of numbers."
            )

        return value

    def validate_email(self, value):
        #this checks if the user with that email already exists in the database
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "A user with this email address already exists."
            )
        return value 

    def create(self, validated_data): 
        user = User.objects.create_user(
            username=validated_data['username'], 
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user