from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=50)
    
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        Author, #the model we are linking to
        on_delete=models.CASCADE, #defines what happens when the referenced object is deleted
        related_name='books'  #Reverse realtion ....allows you to Author.books.all() instead of default Author.books_set.all()
    )
    
class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(
        Book,
        related_name='libraries'
    )
    
class Librarian(models.Model):
    name = models.CharField(max_length=50)
    library = models.OneToOneField(Library, on_delete=models.CASCADE)
    
