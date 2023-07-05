from django.urls import path, include
from .views import get_okr

urlpatterns = [
    path('', get_okr, name='your-name')
]