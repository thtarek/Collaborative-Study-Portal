from django.urls import path, include
from . import views

urlpatterns = [
    path('to-do/', views.to_do, name="to_do"),
    path('to-do/add', views.add_to_do, name="add_to_do"),
]