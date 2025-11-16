import django
import os
from datetime import date

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from accounts.models import CustomUser

def create_test_superuser():
    """Create a test superuser with custom fields"""
    if not CustomUser.objects.filter(username='admin').exists():
        user = CustomUser.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123',
            date_of_birth=date(1990, 1, 1)
        )
        print(f"Superuser created: {user.username}")
        print(f"Email: {user.email}")
        print(f"Date of birth: {user.date_of_birth}")
    else:
        print("Superuser already exists")

if __name__ == "__main__":
    create_test_superuser()