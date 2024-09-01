from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.book_list, name='book_list'),
    path('create_books/', views.create_book, name='create_book'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('update-book/<int:pk>/', views.update_book, name='update_book'),
    path('delete-book/<int:pk>/', views.delete_book, name='delete_book'),
]
