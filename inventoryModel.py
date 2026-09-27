from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet

router = DefaultRouter()
router.register(r'items', ItemViewSet)

urlpatterns =Here is what is going on: you've set up the server successfully, but Django is showing the default rocket page because it hasn't registered your models or custom URLs yet.

Looking closely at your terminal history, a few critical steps were missed due to file locations and file names. Let's fix them step by step!
