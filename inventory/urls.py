from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'items', views.ItemViewSet)

urlpatterns = [
    # Web HTML Views
    path('', views.item_list, name='item_list'),
    path('create/', views.item_create, name='item_create'),
    path('update/<int:pk>/', views.item_update, name='item_update'),
    path('delete/<int:pk>/', views.item_delete, name='item_delete'),
    
    # API Endpoints
    path('api/', include(router.urls)),
]
