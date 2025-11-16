import django
import os

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from django.contrib.auth.models import User
from relationship_app.models import UserProfile

def create_test_users():
    """Create test users with different roles"""
    
    # Create Admin user
    admin_user, created = User.objects.get_or_create(
        username='admin_user',
        defaults={'email': 'admin@example.com'}
    )
    if created:
        admin_user.set_password('password123')
        admin_user.save()
    admin_user.userprofile.role = 'Admin'
    admin_user.userprofile.save()
    
    # Create Librarian user
    librarian_user, created = User.objects.get_or_create(
        username='librarian_user',
        defaults={'email': 'librarian@example.com'}
    )
    if created:
        librarian_user.set_password('password123')
        librarian_user.save()
    librarian_user.userprofile.role = 'Librarian'
    librarian_user.userprofile.save()
    
    # Create Member user
    member_user, created = User.objects.get_or_create(
        username='member_user',
        defaults={'email': 'member@example.com'}
    )
    if created:
        member_user.set_password('password123')
        member_user.save()
    member_user.userprofile.role = 'Member'
    member_user.userprofile.save()
    
    print("Test users created successfully!")
    print("Admin: admin_user / password123")
    print("Librarian: librarian_user / password123")
    print("Member: member_user / password123")
    print("\nRole-based URLs to test:")
    print("Admin: http://127.0.0.1:8000/admin/")
    print("Librarian: http://127.0.0.1:8000/librarian/")
    print("Member: http://127.0.0.1:8000/member/")

if __name__ == "__main__":
    create_test_users()