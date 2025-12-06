# Django Blog Authentication System

## Overview
This authentication system provides comprehensive user management functionality including registration, login, logout, and profile management for the Django blog application.

## Features
- User Registration with email validation
- Secure Login/Logout functionality
- Profile management (edit username, email, first name, last name)
- CSRF protection on all forms
- Responsive navigation based on authentication status
- Success/error message feedback

## Components

### Forms (`blog/forms.py`)
- **CustomUserCreationForm**: Extended Django's UserCreationForm to include email field
- **ProfileUpdateForm**: Allows users to update their profile information

### Views (`blog/views.py`)
- **register**: Handles user registration and automatic login
- **profile**: Login-required view for profile management
- Uses Django's built-in LoginView and LogoutView

### Templates
- **registration/login.html**: User login form
- **registration/register.html**: User registration form
- **registration/profile.html**: Profile editing form
- **blog/base.html**: Updated with authentication navigation

### URLs (`blog/urls.py`)
- `/login/` - User login
- `/logout/` - User logout
- `/register/` - User registration
- `/profile/` - Profile management (login required)

## Security Features
- CSRF tokens on all forms
- Django's built-in password hashing
- Login required decorator for protected views
- Secure password validation

## Setup Instructions

1. **Database Migration** (if needed):
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Create Superuser** (optional):
   ```bash
   python manage.py createsuperuser
   ```

3. **Run Development Server**:
   ```bash
   python manage.py runserver
   ```

## Testing the Authentication System

### Registration Testing
1. Navigate to `/register/`
2. Fill in username, email, and password fields
3. Submit form - should redirect to home page with success message
4. Verify user is automatically logged in

### Login Testing
1. Navigate to `/login/`
2. Enter valid credentials
3. Submit form - should redirect to home page
4. Verify navigation shows user as logged in

### Profile Management Testing
1. Login as a user
2. Navigate to `/profile/`
3. Update profile information
4. Submit form - should show success message
5. Verify changes are saved

### Logout Testing
1. While logged in, click logout link
2. Should redirect to home page
3. Verify navigation shows login/register options

## User Interaction Flow

1. **New User**: Home → Register → Automatic Login → Profile (optional)
2. **Existing User**: Home → Login → Profile (optional) → Logout
3. **Navigation**: Dynamic navigation based on authentication status

## Configuration Settings

The following settings are configured in `settings.py`:
- `LOGIN_REDIRECT_URL = '/'` - Redirect after login
- `LOGOUT_REDIRECT_URL = '/'` - Redirect after logout  
- `LOGIN_URL = '/login/'` - Login page for @login_required decorator

## Error Handling
- Form validation errors are displayed to users
- Invalid login attempts show appropriate error messages
- CSRF protection prevents cross-site request forgery
- Password validation ensures secure passwords

## Customization Options
- Extend User model for additional profile fields
- Add profile pictures using ImageField
- Implement email verification for registration
- Add password reset functionality
- Customize form styling and validation messages