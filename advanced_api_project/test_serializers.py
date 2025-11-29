#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advanced_api_project.settings')
django.setup()

from api.models import Author, Book
from api.serializers import AuthorSerializer, BookSerializer

# Test the serializers
def test_serializers():
    print("Testing Custom Serializers...")
    
    # Create test data
    author = Author.objects.create(name="J.K. Rowling")
    book1 = Book.objects.create(title="Harry Potter", publication_year=1997, author=author)
    book2 = Book.objects.create(title="Fantastic Beasts", publication_year=2001, author=author)
    
    print(f"Created Author: {author}")
    print(f"Created Books: {book1}, {book2}")
    
    # Test BookSerializer
    book_serializer = BookSerializer(book1)
    print(f"\nBookSerializer data: {book_serializer.data}")
    
    # Test AuthorSerializer with nested books
    author_serializer = AuthorSerializer(author)
    print(f"\nAuthorSerializer data: {author_serializer.data}")
    
    # Test validation - future year should fail
    try:
        invalid_book_data = {
            'title': 'Future Book',
            'publication_year': 2030,
            'author': author.id
        }
        invalid_serializer = BookSerializer(data=invalid_book_data)
        if invalid_serializer.is_valid():
            print("ERROR: Future year validation failed!")
        else:
            print(f"\nValidation working: {invalid_serializer.errors}")
    except Exception as e:
        print(f"Validation error: {e}")

if __name__ == "__main__":
    test_serializers()