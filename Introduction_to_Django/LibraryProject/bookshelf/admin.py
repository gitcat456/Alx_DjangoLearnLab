from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # shows these columns
    list_filter = ('publication_year', 'author')  # adds filter sidebar
    search_fields = ('title', 'author')  # adds a search bar