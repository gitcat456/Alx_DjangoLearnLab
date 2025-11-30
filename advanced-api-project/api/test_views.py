import json
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Book
from api.serializers import BookSerializer


class BookAPITestCase(TestCase):
    """Test suite for Book API endpoints"""
    
    def setUp(self):
        """Set up test data and client"""
        # Create test users
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='testpass123'
        )
        self.regular_user = User.objects.create_user(
            username='regular',
            email='regular@example.com',
            password='testpass123'
        )
        
        # Create test books
        self.book1 = Book.objects.create(
            title='The Great Gatsby',
            author='F. Scott Fitzgerald',
            published_year=1925,
            isbn='9780743273565',
            genre='Fiction',
            stock_quantity=10,
            price=12.99
        )
        
        self.book2 = Book.objects.create(
            title='To Kill a Mockingbird',
            author='Harper Lee',
            published_year=1960,
            isbn='9780061120084',
            genre='Fiction',
            stock_quantity=5,
            price=14.99
        )
        
        self.book3 = Book.objects.create(
            title='1984',
            author='George Orwell',
            published_year=1949,
            isbn='9780451524935',
            genre='Dystopian',
            stock_quantity=3,
            price=10.99
        )
        
        # Initialize API client
        self.client = APIClient()
        
        # API endpoints
        self.book_list_url = reverse('book-list')
        self.book_detail_url = lambda pk: reverse('book-detail', kwargs={'pk': pk})

    def test_get_books_list_authenticated(self):
        """Test retrieving books list with authentication"""
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(self.book_list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        
        # Check response data structure
        for book_data in response.data:
            self.assertIn('id', book_data)
            self.assertIn('title', book_data)
            self.assertIn('author', book_data)
            self.assertIn('published_year', book_data)

    def test_get_books_list_unauthenticated(self):
        """Test retrieving books list without authentication"""
        response = self.client.get(self.book_list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_get_single_book_authenticated(self):
        """Test retrieving a single book with authentication"""
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(self.book_detail_url(self.book1.id))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)
        self.assertEqual(response.data['author'], self.book1.author)
        self.assertEqual(response.data['published_year'], self.book1.published_year)

    def test_get_single_book_unauthenticated(self):
        """Test retrieving a single book without authentication"""
        response = self.client.get(self.book_detail_url(self.book1.id))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)

    def test_create_book_authenticated_admin(self):
        """Test creating a book as admin user"""
        self.client.force_authenticate(user=self.admin_user)
        
        new_book_data = {
            'title': 'Brave New World',
            'author': 'Aldous Huxley',
            'published_year': 1932,
            'isbn': '9780060850524',
            'genre': 'Dystopian',
            'stock_quantity': 8,
            'price': 13.50
        }
        
        response = self.client.post(
            self.book_list_url,
            data=json.dumps(new_book_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], new_book_data['title'])
        self.assertEqual(response.data['author'], new_book_data['author'])
        
        # Verify book was created in database
        self.assertTrue(Book.objects.filter(title=new_book_data['title']).exists())

    def test_create_book_authenticated_regular_user(self):
        """Test that regular users cannot create books"""
        self.client.force_authenticate(user=self.regular_user)
        
        new_book_data = {
            'title': 'New Book',
            'author': 'Test Author',
            'published_year': 2023,
            'isbn': '9781234567890',
            'genre': 'Test',
            'stock_quantity': 1,
            'price': 9.99
        }
        
        response = self.client.post(
            self.book_list_url,
            data=json.dumps(new_book_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_book_unauthenticated(self):
        """Test that unauthenticated users cannot create books"""
        new_book_data = {
            'title': 'New Book',
            'author': 'Test Author',
            'published_year': 2023
        }
        
        response = self.client.post(
            self.book_list_url,
            data=json.dumps(new_book_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book_authenticated_admin(self):
        """Test updating a book as admin user"""
        self.client.force_authenticate(user=self.admin_user)
        
        updated_data = {
            'title': 'The Great Gatsby - Updated',
            'author': 'F. Scott Fitzgerald',
            'published_year': 1925,
            'stock_quantity': 15,
            'price': 14.99
        }
        
        response = self.client.put(
            self.book_detail_url(self.book1.id),
            data=json.dumps(updated_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], updated_data['title'])
        self.assertEqual(response.data['stock_quantity'], updated_data['stock_quantity'])
        
        # Verify book was updated in database
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, updated_data['title'])

    def test_update_book_authenticated_regular_user(self):
        """Test that regular users cannot update books"""
        self.client.force_authenticate(user=self.regular_user)
        
        updated_data = {
            'title': 'Updated Title',
            'author': self.book1.author,
            'published_year': self.book1.published_year
        }
        
        response = self.client.put(
            self.book_detail_url(self.book1.id),
            data=json.dumps(updated_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_book_authenticated_admin(self):
        """Test partial update of a book as admin user"""
        self.client.force_authenticate(user=self.admin_user)
        
        partial_data = {
            'stock_quantity': 20,
            'price': 15.99
        }
        
        response = self.client.patch(
            self.book_detail_url(self.book1.id),
            data=json.dumps(partial_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['stock_quantity'], partial_data['stock_quantity'])
        self.assertEqual(response.data['price'], str(partial_data['price']))
        
        # Verify partial update in database
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.stock_quantity, partial_data['stock_quantity'])

    def test_delete_book_authenticated_admin(self):
        """Test deleting a book as admin user"""
        self.client.force_authenticate(user=self.admin_user)
        
        book_to_delete = Book.objects.create(
            title='Temporary Book',
            author='Temp Author',
            published_year=2023,
            stock_quantity=1
        )
        
        response = self.client.delete(self.book_detail_url(book_to_delete.id))
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify book was deleted from database
        self.assertFalse(Book.objects.filter(id=book_to_delete.id).exists())

    def test_delete_book_authenticated_regular_user(self):
        """Test that regular users cannot delete books"""
        self.client.force_authenticate(user=self.regular_user)
        
        response = self.client.delete(self.book_detail_url(self.book1.id))
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_books_by_author(self):
        """Test filtering books by author"""
        response = self.client.get(self.book_list_url, {'author': 'Harper Lee'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'To Kill a Mockingbird')

    def test_filter_books_by_genre(self):
        """Test filtering books by genre"""
        response = self.client.get(self.book_list_url, {'genre': 'Dystopian'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], '1984')

    def test_filter_books_by_published_year(self):
        """Test filtering books by published year"""
        response = self.client.get(self.book_list_url, {'published_year': 1925})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'The Great Gatsby')

    def test_search_books_by_title(self):
        """Test searching books by title"""
        response = self.client.get(self.book_list_url, {'search': 'Mockingbird'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'To Kill a Mockingbird')

    def test_search_books_by_author(self):
        """Test searching books by author"""
        response = self.client.get(self.book_list_url, {'search': 'Fitzgerald'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['author'], 'F. Scott Fitzgerald')

    def test_order_books_by_title(self):
        """Test ordering books by title"""
        response = self.client.get(self.book_list_url, {'ordering': 'title'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles))

    def test_order_books_by_published_year_desc(self):
        """Test ordering books by published year descending"""
        response = self.client.get(self.book_list_url, {'ordering': '-published_year'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['published_year'] for book in response.data]
        self.assertEqual(years, sorted(years, reverse=True))

    def test_order_books_by_price(self):
        """Test ordering books by price"""
        response = self.client.get(self.book_list_url, {'ordering': 'price'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        prices = [float(book['price']) for book in response.data]
        self.assertEqual(prices, sorted(prices))

    def test_invalid_book_creation(self):
        """Test creating a book with invalid data"""
        self.client.force_authenticate(user=self.admin_user)
        
        invalid_data = {
            'title': '',  # Empty title should be invalid
            'author': 'Test Author',
            'published_year': 2023
        }
        
        response = self.client.post(
            self.book_list_url,
            data=json.dumps(invalid_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)

    def test_nonexistent_book_retrieval(self):
        """Test retrieving a non-existent book"""
        response = self.client.get(self.book_detail_url(9999))  # Non-existent ID
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_nonexistent_book(self):
        """Test updating a non-existent book"""
        self.client.force_authenticate(user=self.admin_user)
        
        updated_data = {
            'title': 'Updated Title',
            'author': 'Test Author',
            'published_year': 2023
        }
        
        response = self.client.put(
            self.book_detail_url(9999),  # Non-existent ID
            data=json.dumps(updated_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_stock_quantity_validation(self):
        """Test that stock quantity cannot be negative"""
        self.client.force_authenticate(user=self.admin_user)
        
        invalid_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'published_year': 2023,
            'stock_quantity': -5  # Invalid negative stock
        }
        
        response = self.client.post(
            self.book_list_url,
            data=json.dumps(invalid_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('stock_quantity', response.data)

    def test_published_year_validation(self):
        """Test that published year is reasonable"""
        self.client.force_authenticate(user=self.admin_user)
        
        invalid_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'published_year': 3000  # Invalid future year
        }
        
        response = self.client.post(
            self.book_list_url,
            data=json.dumps(invalid_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('published_year', response.data)


class BookModelTest(TestCase):
    """Test suite for Book model"""
    
    def test_book_creation(self):
        """Test Book model creation"""
        book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            published_year=2023,
            isbn='9781234567890',
            genre='Test Genre',
            stock_quantity=5,
            price=19.99
        )
        
        self.assertEqual(book.title, 'Test Book')
        self.assertEqual(book.author, 'Test Author')
        self.assertEqual(book.published_year, 2023)
        self.assertEqual(book.stock_quantity, 5)
        self.assertEqual(str(book), 'Test Book by Test Author')

    def test_book_string_representation(self):
        """Test Book model string representation"""
        book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            published_year=2023
        )
        
        self.assertEqual(str(book), 'Test Book by Test Author')