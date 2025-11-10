from django.shortcuts import render
from  relationship_app.models import Book
from .models import Library
from django.views.generic import DetailView

def book_list(request):
    all_books = Book.objects.all()
    context = {'books': all_books}
    return render(request, 'relationship_app/list_books.html', context)
    

class LibBooks(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    
    
