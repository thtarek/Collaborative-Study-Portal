from django.urls import path, include
from . import views

urlpatterns = [
    path('to-do/', views.to_do, name="to_do"),
    path('to-do/add', views.add_to_do, name="add_to_do"),
    path('to-do/delete/<int:pk>/', views.delete_todo, name="delete_todo"),
    path('to-do/complete/<int:pk>/', views.complete_todo, name="complete_todo"),
    path('to-do/edit-todo/<int:pk>/', views.edit_todo, name="edit_todo"),
]