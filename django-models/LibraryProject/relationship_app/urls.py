from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.book_list, name='book_list'),
    path('library/<int:pk>/', views.LibBooks.as_view(), name='library_detail')
]