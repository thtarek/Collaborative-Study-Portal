from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.user_login, name='user_login'),
    path('user-logout/', views.user_logout, name='user_logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
]