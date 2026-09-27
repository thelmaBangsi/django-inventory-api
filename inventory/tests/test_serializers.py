from django.test import TestCase 
from django.contrib.auth.models import User
from inventory.serializers.user_serializers import RegisterSerializer 

class RegisterSerializerTests(TestCase): 
    def test_valid_user_registration(self): 
        data = {"username": "ValidUser1", "email": "valid@gmail.com", "password": "password123"}
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, "ValidUser1")

    def test_username_cannot_contain_invalid_symbols(self):
        data = {"username": "-1", "email": "test@gmail.com", "password": "password123"}
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("username", serializer.errors)


    def test_username_cannot_consist_solely_of_digits(self):
        data = {"username": "12345", "email": "test@gmail.com", "password": "password123"}
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("username", serializer.errors)

    def test_email_must_be_unique(self): 
        User.objects.create_user(username="UserOne", email="duplicate@gmail.com", password="password123")
        data = {"username": "UserTwo", "email": "duplicate@gmail.com", "password": "password123"}
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)
