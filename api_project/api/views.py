from .models import Book
from .serializers import BookSerializer 
from rest_framework import generics, viewsets

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
class BookList(generics.ListCreateAPIView):
    serializer_class = BookSerializer
    
    def get_queryset(self):
        queryset = Book.objects.all()
        search = self.request.query_params.get('search', None)
        if search is not None:
            queryset = queryset.filter(title__icontains=search)
        return queryset

class BookUpdate(generics.RetrieveUpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookDelete(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer























































































# from django.shortcuts import render
# from rest_framework import generics, viewsets
# from .serializers import BookSerializer
# from .models import Book
# #from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny, IsAuthenticatedOrReadOnly

# class BookList(generics.ListAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#     #permission_classes = [AllowAny]

# class BookViewSet(viewsets.ModelViewSet):
#      queryset = Book.objects.all()
#      serializer_class = BookSerializer
#     # permission_classes = [IsAuthenticatedOrReadOnly] 
    
#     # def get_permissions(self):
#         #if self.action == 'list' or self.action == 'retrieve':
#            # permission_classes = [AllowAny]
#        # else:
#             #permission_classes = [IsAuthenticated]
#        # return [permission() for permission in permission_classes]