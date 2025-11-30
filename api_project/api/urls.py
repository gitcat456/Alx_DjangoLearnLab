from .views import BookList, BookUpdate, BookDelete, BookViewSet
from django.urls import path,include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'viewset_books', BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('books/', BookList.as_view(), name='books'),
    path('book/<int:pk>/update', BookUpdate.as_view(), name='book_update'),
    path('book/delete/<int:pk>', BookDelete.as_view(), name='book_delete'),
]






























































# from django.urls import path, include
# from .views import BookList, BookViewSet
# from rest_framework.routers import DefaultRouter
# from rest_framework.authtoken.views import obtain_auth_token

# router = DefaultRouter()
# router.register(r'books_all', BookViewSet, basename='book_all')

# urlpatterns = [
#     path('books/', BookList.as_view(), name='book-list'),
#     path('', include(router.urls)),
#    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
# ]