# retrieve.md
```python
from bookshelf.models import Book
books = Book.objects.all()
for b in books:
    print(b.title, b.author, b.publication_year)
# Output:
# 1984 George Orwell 1949
