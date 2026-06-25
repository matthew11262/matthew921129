# 確保你的 urls.py 裡引用的 API 名稱符合我們新的 views.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/latest/', views.api_latest, name='api_latest'),
    path('api/records/', views.api_records, name='api_records'),
    path('api/history/', views.api_history, name='api_history'), # 留著沒關係，新 views 有寫空回傳
    path('api/button/status/', views.api_button_status, name='api_button_status'),
    path('api/button/history/', views.api_button_history, name='api_button_history'),
]