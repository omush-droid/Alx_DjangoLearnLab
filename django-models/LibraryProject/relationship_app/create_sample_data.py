import django
import os

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# Create sample data for testing views
def create_sample_data():
    # Create authors
    author1, created = Author.objects.get_or_create(name="J.K. Rowling")
    author2, created = Author.objects.get_or_create(name="George Orwell")
    
    # Create books
    book1, created = Book.objects.get_or_create(title="Harry Potter and the Philosopher's Stone", author=author1)
    book2, created = Book.objects.get_or_create(title="1984", author=author2)
    book3, created = Book.objects.get_or_create(title="Animal Farm", author=author2)
    
    # Create library
    library, created = Library.objects.get_or_create(name="Central Library")
    library.books.add(book1, book2, book3)
    
    # Create librarian
    librarian, created = Librarian.objects.get_or_create(name="Alice Smith", library=library)
    
    print("Sample data created successfully!")
    print(f"Authors: {Author.objects.count()}")
    print(f"Books: {Book.objects.count()}")
    print(f"Libraries: {Library.objects.count()}")
    print(f"Librarians: {Librarian.objects.count()}")

if __name__ == "__main__":
    create_sample_data()