import django
import os

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book, CustomUser

def setup_groups_and_permissions():
    """Create groups and assign permissions for book management"""
    
    # Get book permissions
    content_type = ContentType.objects.get_for_model(Book)
    can_view = Permission.objects.get(codename='can_view', content_type=content_type)
    can_create = Permission.objects.get(codename='can_create', content_type=content_type)
    can_edit = Permission.objects.get(codename='can_edit', content_type=content_type)
    can_delete = Permission.objects.get(codename='can_delete', content_type=content_type)
    
    # Create Viewers group
    viewers_group, created = Group.objects.get_or_create(name='Viewers')
    if created:
        viewers_group.permissions.add(can_view)
        print("Created Viewers group with can_view permission")
    
    # Create Editors group
    editors_group, created = Group.objects.get_or_create(name='Editors')
    if created:
        editors_group.permissions.add(can_view, can_create, can_edit)
        print("Created Editors group with can_view, can_create, can_edit permissions")
    
    # Create Admins group
    admins_group, created = Group.objects.get_or_create(name='Admins')
    if created:
        admins_group.permissions.add(can_view, can_create, can_edit, can_delete)
        print("Created Admins group with all permissions")
    
    # Create test users
    viewer_user, created = CustomUser.objects.get_or_create(
        username='viewer_user',
        defaults={'email': 'viewer@example.com'}
    )
    if created:
        viewer_user.set_password('password123')
        viewer_user.save()
        viewer_user.groups.add(viewers_group)
        print("Created viewer_user and added to Viewers group")
    
    editor_user, created = CustomUser.objects.get_or_create(
        username='editor_user',
        defaults={'email': 'editor@example.com'}
    )
    if created:
        editor_user.set_password('password123')
        editor_user.save()
        editor_user.groups.add(editors_group)
        print("Created editor_user and added to Editors group")
    
    admin_user, created = CustomUser.objects.get_or_create(
        username='admin_user',
        defaults={'email': 'admin@example.com'}
    )
    if created:
        admin_user.set_password('password123')
        admin_user.save()
        admin_user.groups.add(admins_group)
        print("Created admin_user and added to Admins group")
    
    print("\\nGroups and permissions setup complete!")
    print("Test users created with password: password123")
    print("- viewer_user (Viewers group)")
    print("- editor_user (Editors group)")
    print("- admin_user (Admins group)")

if __name__ == "__main__":
    setup_groups_and_permissions()