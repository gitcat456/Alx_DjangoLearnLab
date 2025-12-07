from django.urls import path
from .models import Post
from .views import RegisterView,ProfileUpdateView
from django.contrib.auth.views import LoginView, LogoutView
from . import views
urlpatterns = [
     path('posts/', views.PostListView.as_view(), name='post-list'),
    path('posts/new/', views.PostCreateView.as_view(), name='post-create'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post-update'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    
    path('register/', RegisterView.as_view(), name='register' ),
    path('login/', LoginView.as_view(template_name='blog/login.html'), name='login' ),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout' ),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
]