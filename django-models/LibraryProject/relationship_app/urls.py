from django.urls import path
from . import views
from .views import LibBooks, book_list

urlpatterns = [
    path('books/', views.book_list, name='book_list'),
    path('library/<int:pk>/', LibBooks.as_view(), name='library_detail')
]