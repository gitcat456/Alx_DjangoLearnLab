from relationship_app.models import Author, Book, Library, Librarian

author = Author.objects.get(name="J.K. Rowling")  # get that author object
books_by_author = author.books.all()  # use related_name to get all books
print("Books by author:", list(books_by_author))
#or Book.objects.filter(author__name="J.K. Rowling")


library = Library.objects.get(name="Central Library")
books_in_library = library.books.all()  # ManyToManyField reverse access
# or from book>libraries : book.libraries.all()
print("Books in library:", list(books_in_library))

librarian = library.librarian
print(f"Librarian for {library.name}: {librarian.name}")

