from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.user_login, name='user_login'),
    path('create-account', views.create_account, name='create_account'),
    path('user-logout/', views.user_logout, name='user_logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
]