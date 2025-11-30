from django.urls import path
from .views import(
    BookListView,
    BookCreateView,
    BookDetailView,
    BookUpdateView,
    BookDeleteView
)

urlpatterns = [
    path('books/', BookListView.as_view()),
    path('books/', BookCreateView.as_view()),
    path('books/<int:pk>/', BookDetailView.as_view()),
    path('books/<int:pk>/update/', BookUpdateView.as_view()),
    path('books/<int:pk>/delete/', BookListView.as_view()),
]