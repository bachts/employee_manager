from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    #path('okr/get', views.get_okr, name='get-okr'),
    path('log/', views.log_list, name='log-list'),
    path('log/<int:pk>/', views.log_detail, name='log-detail')
]

urlpatterns = format_suffix_patterns(urlpatterns)