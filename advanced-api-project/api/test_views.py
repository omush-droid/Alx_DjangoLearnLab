from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Author, Book

class BookAPITestCase(TestCase):
    def setUp(self):
        """Set up test data and client"""
        self.client = APIClient()
        
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create test author
        self.author = Author.objects.create(name='Test Author')
        
        # Create test book
        self.book = Book.objects.create(
            title='Test Book',
            publication_year=2023,
            author=self.author
        )

    def test_book_list_view(self):
        """Test retrieving list of books"""
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_book_detail_view(self):
        """Test retrieving a single book"""
        response = self.client.get(f'/api/books/{self.book.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Book')

    def test_book_create_authenticated(self):
        """Test creating a book with authentication"""
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'New Book',
            'publication_year': 2024,
            'author': self.author.id
        }
        response = self.client.post('/api/books/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_book_create_unauthenticated(self):
        """Test creating a book without authentication"""
        data = {
            'title': 'New Book',
            'publication_year': 2024,
            'author': self.author.id
        }
        response = self.client.post('/api/books/create/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_book_update_authenticated(self):
        """Test updating a book with authentication"""
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Updated Book',
            'publication_year': 2024,
            'author': self.author.id
        }
        response = self.client.put(f'/api/books/update/{self.book.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Book')

    def test_book_update_unauthenticated(self):
        """Test updating a book without authentication"""
        data = {
            'title': 'Updated Book',
            'publication_year': 2024,
            'author': self.author.id
        }
        response = self.client.put(f'/api/books/update/{self.book.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_book_delete_authenticated(self):
        """Test deleting a book with authentication"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/books/delete/{self.book.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_book_delete_unauthenticated(self):
        """Test deleting a book without authentication"""
        response = self.client.delete(f'/api/books/delete/{self.book.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_book_filtering(self):
        """Test filtering books by publication year"""
        response = self.client.get('/api/books/?publication_year=2023')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_book_search(self):
        """Test searching books by title"""
        response = self.client.get('/api/books/?search=Test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_book_ordering(self):
        """Test ordering books by title"""
        # Create another book for ordering test
        Book.objects.create(
            title='Another Book',
            publication_year=2022,
            author=self.author
        )
        response = self.client.get('/api/books/?ordering=title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Another Book')