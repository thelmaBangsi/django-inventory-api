from django.urls import path
from .views import (
    register_user,
    login_user,
    forgot_password,
    dashboard,
    list_users,
    update_user_profile,
)

urlpatterns = [
    # Auth Endpoints
    path('auth/register/', register_user, name='register'),
    path('auth/login/', login_user, name='login'),
    path('auth/forgot-password/', forgot_password, name='forgot_password'),

    # User Management Endpoints
    path('dashboard/', dashboard, name='dashboard'),
    path('users/', list_users, name='list_users'),
    path('users/<int:user_id>/', update_user_profile, name='update_user_profile'),
]
