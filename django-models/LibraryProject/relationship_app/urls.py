from django.urls import path
from . import views
from .views import (list_books, LibraryDetailView, admin_view, 
                   librarian_view, member_view, add_book, edit_book, delete_book)
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
)

urlpatterns = [
    #path('register/', SignUpView.as_view(), name='register'),
    path('register/', views.register, name='register'), 
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('books/', list_books, name='book_list'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    
     # Role-based URLs
    path('admin/dashboard/', admin_view, name='admin_view'),
    path('librarian/dashboard/', librarian_view, name='librarian_view'),
    path('member/dashboard/', member_view, name='member_view'),
    
     # SECURED BOOK MANAGEMENT URLS
    path('books/add/', add_book, name='add_book'),
    path('books/<int:book_id>/edit/', edit_book, name='edit_book'),
    path('books/<int:book_id>/delete/', delete_book, name='delete_book'),
]