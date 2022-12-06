from django.urls import path, include
from . import views

urlpatterns = [
    path('to-do/', views.to_do, name="to_do"),
    path('to-do/add', views.add_to_do, name="add_to_do"),
    path('to-do/delete/<int:pk>/', views.delete_todo, name="delete_todo"),
    path('to-do/complete/<int:pk>/', views.complete_todo, name="complete_todo"),
    path('to-do/edit-todo/<int:pk>/', views.edit_todo, name="edit_todo"),

    # YOUTUBE SEARCH

    path('youtube', views.youtube_search, name='youtube_search'),
    path('weather/', views.weather_update, name='weather_update'),
    path('book/', views.search_book, name='search_book'),
    path('book-detail/<id>/', views.book_detail, name='book_detail'),
]