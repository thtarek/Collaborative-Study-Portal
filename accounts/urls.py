from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.user_login, name='user_login'),
    path('dashboard/', views.dashboard, name='dashboard'),
]