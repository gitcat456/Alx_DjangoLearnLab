from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Notification

class NotificationListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)
    
    def list(self, request):
        notifications = self.get_queryset()
        data = []
        for notification in notifications:
            data.append({
                'id': notification.id,
                'actor': notification.actor.username,
                'verb': notification.verb,
                'read': notification.read,
                'timestamp': notification.timestamp
            })
        return Response(data)