from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import (
    ChangePasswordSerializer,
    PasswordResetRequestSerializer,
    RegisterSerializer,
    UserSerializer,
)


# ==========================================
# PUBLIC ENDPOINTS (No Token Required)
# ==========================================

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def register_user(request):
    """
    Public endpoint to register a new user with unique email enforcement.
    """
    if request.method == 'GET':
        return Response(
            {"message": "Send a POST request with username, email, and password to register."}
        )

    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(
            {
                "message": "User registered successfully.",
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def login_user(request):
    """
    Public session/basic login endpoint.
    """
    if request.method == 'GET':
        return Response(
            {"message": "Send a POST request with username and password to log in."}
        )

    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)

    if user is not None:
        return Response(
            {
                "message": "Login successful",
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )
    return Response(
        {"error": "Invalid username or password"},
        status=status.HTTP_401_UNAUTHORIZED,
    )


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def forgot_password(request):
    """
    Public endpoint to trigger password reset.
    """
    if request.method == 'GET':
        return Response(
            {"message": "Send a POST request with email to request a password reset."}
        )

    serializer = PasswordResetRequestSerializer(data=request.data)
    if serializer.is_valid():
        return Response(
            {"message": "Password reset link sent to your email."},
            status=status.HTTP_200_OK,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ==========================================
# PROTECTED ENDPOINTS (JWT Token Required)
# ==========================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    """
    Protected dashboard endpoint.
    """
    return Response(
        {
            "message": f"Welcome to the inventory dashboard, {request.user.username}!",
            "user_id": request.user.id,
        },
        status=status.HTTP_200_OK,
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_users(request):
    """
    Protected endpoint to list all registered users.
    """
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_user_profile(request, user_id):
    """
    Protected endpoint to retrieve or update a user profile.
    """
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method in ['PUT', 'PATCH']:
        if 'old_password' in request.data and 'new_password' in request.data:
            pw_serializer = ChangePasswordSerializer(data=request.data)
            if pw_serializer.is_valid():
                if not user.check_password(pw_serializer.data.get('old_password')):
                    return Response(
                        {"error": "Wrong old password."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                user.set_password(pw_serializer.data.get('new_password'))
                user.save()
                return Response(
                    {"message": "Password updated successfully."},
                    status=status.HTTP_200_OK,
                )
            return Response(
                pw_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Profile updated successfully.",
                    "user": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
