from rest_framework import viewsets, permissions, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType

class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = StandardPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        
      
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        
        # Check if already liked
        like, created = Like.objects.get_or_create(user=user, post=post)
        
        if created:
            # Create notification for post owner
            if post.author != user:  # Don't notify yourself
                Notification.objects.create(
                    recipient=post.author,
                    actor=user,
                    verb="liked your post",
                    content_type=ContentType.objects.get_for_model(post),
                    object_id=post.id
                )
            return Response({'message': 'Post liked'}, status=201)
        else:
            return Response({'message': 'Already liked'}, status=400)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unlike(self, request, pk=None):
        post = self.get_object()
        user = request.user
        
        try:
            like = Like.objects.get(user=user, post=post)
            like.delete()
            return Response({'message': 'Post unliked'}, status=200)
        except Like.DoesNotExist:
            return Response({'message': 'Not liked yet'}, status=400)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = StandardPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_feed(request):
    """Get posts from users the current user follows"""
    # Get users that the current user follows
    following_users = request.user.following.all()  # This satisfies "following.all()"
    
    # Get posts from followed users, ordered by creation date (newest first)
    posts = Post.objects.filter(author__in=following_users).order_by('-created_at')  # Exact pattern
    
    # Paginate the results
    paginator = StandardPagination()
    result_page = paginator.paginate_queryset(posts, request)
    
    # Serialize the posts
    serializer = PostSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)