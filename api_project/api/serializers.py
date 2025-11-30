from rest_framework import serializers
from .models import Book
from django.utils import timezone

class BookSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    
    class Meta:
        model=Book
        fields=['id', 'title', 'author', 'published_date', 'created_at']
        
    def get_created_at(self, obj):
        return timezone.now().strftime('%Y-%m-%d %H:%M:%S')