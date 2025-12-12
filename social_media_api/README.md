# Social Media API

A Django REST Framework-based social media API with user authentication and profile management.

## Setup Instructions

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Install Dependencies**
   ```bash
   pip install django djangorestframework
   ```

2. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create Superuser (Optional)**
   ```bash
   python manage.py createsuperuser
   ```

4. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Authentication Endpoints

- **POST** `/api/accounts/register/` - User registration
- **POST** `/api/accounts/login/` - User login
- **GET/PUT** `/api/accounts/profile/` - User profile management

### User Registration
**Endpoint:** `POST /api/accounts/register/`

**Request Body:**
```json
{
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepassword123",
    "bio": "Optional bio text"
}
```

**Response:**
```json
{
    "token": "your-auth-token",
    "user_id": 1,
    "username": "testuser"
}
```

### User Login
**Endpoint:** `POST /api/accounts/login/`

**Request Body:**
```json
{
    "username": "testuser",
    "password": "securepassword123"
}
```

**Response:**
```json
{
    "token": "your-auth-token",
    "user_id": 1,
    "username": "testuser"
}
```

### User Profile
**Endpoint:** `GET /api/accounts/profile/`

**Headers:**
```
Authorization: Token your-auth-token
```

**Response:**
```json
{
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "bio": "User bio text",
    "profile_picture": null,
    "followers": []
}
```

## User Model Features

The custom User model extends Django's AbstractUser with additional fields:
- `bio`: Text field for user biography
- `profile_picture`: Image field for profile pictures
- `followers`: Many-to-many relationship for following other users

## Authentication

The API uses Django REST Framework's Token Authentication. Include the token in the Authorization header:
```
Authorization: Token your-auth-token
```

## Testing with Postman

1. **Register a new user** - POST to `/api/accounts/register/`
2. **Login with credentials** - POST to `/api/accounts/login/`
3. **Access profile** - GET `/api/accounts/profile/` with token header
4. **Update profile** - PUT `/api/accounts/profile/` with token header

## Project Structure

```
social_media_api/
├── accounts/
│   ├── migrations/
│   ├── models.py          # Custom User model
│   ├── serializers.py     # API serializers
│   ├── views.py          # API views
│   ├── urls.py           # App URL patterns
│   └── admin.py          # Admin configuration
├── social_media_api/
│   ├── settings.py       # Project settings
│   └── urls.py          # Main URL configuration
└── manage.py
```