from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/latest/', views.api_latest, name='api_latest'),
    path('api/history/', views.api_history, name='api_history'),
    path('api/records/', views.api_records, name='api_records'),
    path('api/button/status/', views.api_button_status, name='api_button_status'),
    path('api/button/history/', views.api_button_history, name='api_button_history'),
]
