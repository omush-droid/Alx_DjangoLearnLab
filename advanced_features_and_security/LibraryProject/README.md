# Django Permissions and Groups System

## Overview
This Django application implements a comprehensive permissions and groups system to control access to book management functionality.

## Custom Permissions
The Book model includes four custom permissions:
- `can_view`: Permission to view books
- `can_create`: Permission to create new books
- `can_edit`: Permission to edit existing books
- `can_delete`: Permission to delete books

## Groups Setup
Create the following groups in Django Admin and assign permissions:

### Viewers Group
- Permissions: `can_view`
- Purpose: Users can only view books

### Editors Group
- Permissions: `can_view`, `can_create`, `can_edit`
- Purpose: Users can view, create, and edit books

### Admins Group
- Permissions: `can_view`, `can_create`, `can_edit`, `can_delete`
- Purpose: Users have full access to all book operations

## Permission-Protected Views
All views use the `@permission_required` decorator:
- `book_list`: Requires `bookshelf.can_view`
- `book_create`: Requires `bookshelf.can_create`
- `book_edit`: Requires `bookshelf.can_edit`
- `book_delete`: Requires `bookshelf.can_delete`

## Setup Instructions
1. Run migrations: `python manage.py migrate`
2. Create superuser: `python manage.py createsuperuser`
3. Access admin at `/admin/` to create groups and assign permissions
4. Create test users and assign them to groups
5. Test access at `/books/`

## Testing
- Create users in different groups
- Login as each user type
- Verify access restrictions are enforced
- Users without proper permissions will see permission denied errors