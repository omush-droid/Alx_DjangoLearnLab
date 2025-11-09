import django
import os

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from relationship_app.models import Book

def assign_permissions():
    """Assign book permissions to users based on their roles"""
    
    # Get book permissions
    content_type = ContentType.objects.get_for_model(Book)
    can_add_book = Permission.objects.get(codename='can_add_book', content_type=content_type)
    can_change_book = Permission.objects.get(codename='can_change_book', content_type=content_type)
    can_delete_book = Permission.objects.get(codename='can_delete_book', content_type=content_type)
    
    # Assign permissions to Admin users
    admin_users = User.objects.filter(userprofile__role='Admin')
    for user in admin_users:
        user.user_permissions.add(can_add_book, can_change_book, can_delete_book)
        print(f"Assigned all book permissions to Admin: {user.username}")
    
    # Assign permissions to Librarian users
    librarian_users = User.objects.filter(userprofile__role='Librarian')
    for user in librarian_users:
        user.user_permissions.add(can_add_book, can_change_book)
        print(f"Assigned add/change book permissions to Librarian: {user.username}")
    
    print("Permissions assigned successfully!")
    print("\nTest URLs:")
    print("Add Book: http://127.0.0.1:8000/add_book/")
    print("Edit Book: http://127.0.0.1:8000/edit_book/1/")
    print("Delete Book: http://127.0.0.1:8000/delete_book/1/")

if __name__ == "__main__":
    assign_permissions()