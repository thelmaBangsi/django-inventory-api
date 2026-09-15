from django.urls import path
from . import views

urlpatterns = [
    # Web HTML Routes
    path('', views.item_list, name='item_list'),
    path('create/', views.item_create, name='item_create'),
    path('update/<int:pk>/', views.item_update, name='item_update'),
    path('delete/<int:pk>/', views.item_delete, name='item_delete'),

    # REST API Endpoints (Use these with cURL and JWT)
    path('api/items/', views.api_item_list, name='api_item_list'),
    path('api/create/', views.api_item_create, name='api_item_create'),
    path('api/update/<int:pk>/', views.api_item_update, name='api_item_update'),
    path('api/delete/<int:pk>/', views.api_item_delete, name='api_item_delete'),
]
