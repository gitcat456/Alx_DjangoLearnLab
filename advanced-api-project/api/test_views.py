import json
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Book
from api.serializers import BookSerializer


class BookAPITestCase(TestCase):
    """Test suite for Book API endpoints with proper test database setup"""
    
    def setUp(self):
        """Set up test data and client with proper test database configuration"""
        # Verify we're using test database
        self.assertIn('test', settings.DATABASES['default']['NAME'], 
                     "Not using test database! Check your test configuration.")
        
        # Create test users using proper authentication methods
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

    def tearDown(self):
        """Clean up after tests - test database is automatically destroyed"""
        # The test database is automatically destroyed after tests
        # This is just to demonstrate proper test isolation
        Book.objects.all().delete()
        User.objects.all().delete()

    def test_database_isolation(self):
        """Verify we're using test database and data is isolated"""
        # This test verifies that our test data is isolated
        initial_book_count = Book.objects.count()
        self.assertEqual(initial_book_count, 3, 
                        "Test data not properly set up or database not isolated")

    # Authentication tests using client.login() method
    def test_get_books_list_with_login(self):
        """Test retrieving books list with login authentication"""
        # Using client.login() for session-based authentication
        login_success = self.client.login(username='regular', password='testpass123')
        self.assertTrue(login_success, "User login failed")
        
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        
        # Logout after test
        self.client.logout()

    def test_create_book_with_admin_login(self):
        """Test creating a book with admin login"""
        # Login as admin user
        login_success = self.client.login(username='admin', password='testpass123')
        self.assertTrue(login_success, "Admin login failed")
        
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
        self.assertEqual(Book.objects.count(), 4)  # Should have one more book
        
        # Logout after test
        self.client.logout()

    def test_create_book_with_regular_user_login(self):
        """Test that regular users cannot create books using login"""
        login_success = self.client.login(username='regular', password='testpass123')
        self.assertTrue(login_success, "Regular user login failed")
        
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
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.logout()

    def test_update_book_with_admin_login(self):
        """Test updating a book with admin login"""
        login_success = self.client.login(username='admin', password='testpass123')
        self.assertTrue(login_success, "Admin login failed")
        
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
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'The Great Gatsby - Updated')
        
        self.client.logout()

    def test_delete_book_with_admin_login(self):
        """Test deleting a book with admin login"""
        login_success = self.client.login(username='admin', password='testpass123')
        self.assertTrue(login_success, "Admin login failed")
        
        book_to_delete = Book.objects.create(
            title='Temporary Book',
            author='Temp Author',
            published_year=2023
        )
        
        initial_count = Book.objects.count()
        response = self.client.delete(self.book_detail_url(book_to_delete.id))
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), initial_count - 1)
        
        self.client.logout()

    def test_access_without_login(self):
        """Test that some endpoints are accessible without login"""
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_protected_endpoints_without_login(self):
        """Test that protected endpoints require authentication"""
        new_book_data = {
            'title': 'New Book',
            'author': 'Test Author',
            'published_year': 2023
        }
        
        # Try to create book without login
        response = self.client.post(
            self.book_list_url,
            data=json.dumps(new_book_data),
            content_type='application/json'
        )
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    # Keep some tests using force_authenticate for token-based auth
    def test_get_books_list_authenticated_token(self):
        """Test retrieving books list with token authentication"""
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.force_authenticate(user=None)  # Remove authentication

    def test_create_book_authenticated_admin_token(self):
        """Test creating a book as admin user with token auth"""
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
        self.client.force_authenticate(user=None)

    # Filtering and searching tests (no authentication required)
    def test_filter_books_by_author(self):
        """Test filtering books by author"""
        response = self.client.get(self.book_list_url, {'author': 'Harper Lee'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'To Kill a Mockingbird')

    def test_search_books_by_title(self):
        """Test searching books by title"""
        response = self.client.get(self.book_list_url, {'search': 'Mockingbird'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'To Kill a Mockingbird')

    def test_order_books_by_title(self):
        """Test ordering books by title"""
        response = self.client.get(self.book_list_url, {'ordering': 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles))

    # Validation tests
    def test_invalid_book_creation_with_login(self):
        """Test creating a book with invalid data using login"""
        login_success = self.client.login(username='admin', password='testpass123')
        self.assertTrue(login_success, "Admin login failed")
        
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
        self.client.logout()


class TestDatabaseConfiguration(TestCase):
    """Specific tests to verify test database configuration"""
    
    def test_test_database_name(self):
        """Verify we're using test database"""
        db_name = settings.DATABASES['default']['NAME']
        self.assertIn('test', db_name, 
                     f"Not using test database! Current database: {db_name}")
    
    def test_database_isolation(self):
        """Test that database is properly isolated between test cases"""
        # This should be empty in a fresh test case
        self.assertEqual(Book.objects.count(), 0)
        self.assertEqual(User.objects.count(), 0)
        
        # Create some test data
        Book.objects.create(
            title='Test Book',
            author='Test Author',
            published_year=2023
        )
        User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        
        # Verify data was created
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(User.objects.count(), 1)


# Test configuration verification
def test_suite_configuration():
    """Function to verify test suite is properly configured"""
    import sys
    print(f"Python executable: {sys.executable}")
    print(f"Database in use: {settings.DATABASES['default']['NAME']}")
    print(f"DEBUG mode: {settings.DEBUG}")