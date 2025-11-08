import django
import os

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def query_books_by_author(author_name):
    """Query all books by a specific author."""
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        return books
    except Author.DoesNotExist:
        return None

def list_books_in_library(library_name):
    """List all books in a library."""
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        return books
    except Library.DoesNotExist:
        return None

def get_librarian_for_library(library_name):
    """Retrieve the librarian for a library."""
    try:
        library = Library.objects.get(name=library_name)
        librarian = Librarian.objects.get(library=library)
        return librarian
    except (Library.DoesNotExist, Librarian.DoesNotExist):
        return None

# Sample usage (uncomment to test)
if __name__ == "__main__":
    # Create sample data
    author1 = Author.objects.create(name="J.K. Rowling")
    author2 = Author.objects.create(name="George Orwell")
    
    book1 = Book.objects.create(title="Harry Potter", author=author1)
    book2 = Book.objects.create(title="1984", author=author2)
    
    library = Library.objects.create(name="Central Library")
    library.books.add(book1, book2)
    
    librarian = Librarian.objects.create(name="Alice Smith", library=library)
    
    # Test queries
    print("Books by J.K. Rowling:", [book.title for book in query_books_by_author("J.K. Rowling")])
    print("Books in Central Library:", [book.title for book in list_books_in_library("Central Library")])
    print("Librarian for Central Library:", get_librarian_for_library("Central Library").name)