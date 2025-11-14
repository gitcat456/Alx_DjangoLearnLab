from django.urls import path
from . import views
from .views import (
    SignUpView,
    list_books, 
    LibraryDetailView, 
    )
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
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail')
]