from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/latest/', views.api_latest, name='api_latest'),
    path('api/history/', views.api_history, name='api_history'),
    path('api/records/', views.api_records, name='api_records'),
]
