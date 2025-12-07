from django.urls import path
from .models import Post
from .views import RegisterView,ProfileUpdateView
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register' ),
    path('login/', LoginView.as_view(template_name='blog/login.html'), name='login' ),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout' ),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
]