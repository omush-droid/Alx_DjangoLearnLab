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

### Posts Endpoints

- **GET** `/api/posts/` - List all posts (with pagination and search)
- **POST** `/api/posts/` - Create a new post
- **GET** `/api/posts/{id}/` - Retrieve a specific post
- **PUT** `/api/posts/{id}/` - Update a post (author only)
- **DELETE** `/api/posts/{id}/` - Delete a post (author only)

### Comments Endpoints

- **GET** `/api/comments/` - List all comments (with filtering)
- **POST** `/api/comments/` - Create a new comment
- **GET** `/api/comments/{id}/` - Retrieve a specific comment
- **PUT** `/api/comments/{id}/` - Update a comment (author only)
- **DELETE** `/api/comments/{id}/` - Delete a comment (author only)

### Follow System Endpoints

- **POST** `/api/accounts/follow/{user_id}/` - Follow a user
- **POST** `/api/accounts/unfollow/{user_id}/` - Unfollow a user

### Feed Endpoints

- **GET** `/api/feed/` - Get personalized feed of posts from followed users

### Likes Endpoints

- **POST** `/api/posts/{id}/like/` - Like a post
- **POST** `/api/posts/{id}/unlike/` - Unlike a post

### Notifications Endpoints

- **GET** `/api/notifications/` - Get user's notifications
- **POST** `/api/notifications/{id}/read/` - Mark notification as read

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

### Create Post
**Endpoint:** `POST /api/posts/`

**Headers:**
```
Authorization: Token your-auth-token
Content-Type: application/json
```

**Request Body:**
```json
{
    "title": "My First Post",
    "content": "This is the content of my first post."
}
```

**Response:**
```json
{
    "id": 1,
    "author": "testuser",
    "title": "My First Post",
    "content": "This is the content of my first post.",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z",
    "comments_count": 0
}
```

### List Posts with Search
**Endpoint:** `GET /api/posts/?search=keyword&page=1`

**Response:**
```json
{
    "count": 25,
    "next": "http://localhost:8000/api/posts/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "author": "testuser",
            "title": "My First Post",
            "content": "This is the content of my first post.",
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-15T10:30:00Z",
            "comments_count": 2
        }
    ]
}
```

### Create Comment
**Endpoint:** `POST /api/comments/`

**Headers:**
```
Authorization: Token your-auth-token
Content-Type: application/json
```

**Request Body:**
```json
{
    "post": 1,
    "content": "Great post! Thanks for sharing."
}
```

**Response:**
```json
{
    "id": 1,
    "post": 1,
    "author": "testuser",
    "content": "Great post! Thanks for sharing.",
    "created_at": "2024-01-15T10:35:00Z",
    "updated_at": "2024-01-15T10:35:00Z"
}
```

### Follow User
**Endpoint:** `POST /api/accounts/follow/{user_id}/`

**Headers:**
```
Authorization: Token your-auth-token
```

**Response:**
```json
{
    "message": "Now following username"
}
```

### Unfollow User
**Endpoint:** `POST /api/accounts/unfollow/{user_id}/`

**Headers:**
```
Authorization: Token your-auth-token
```

**Response:**
```json
{
    "message": "Unfollowed username"
}
```

### Get Feed
**Endpoint:** `GET /api/feed/`

**Headers:**
```
Authorization: Token your-auth-token
```

**Response:**
```json
[
    {
        "id": 1,
        "author": "followed_user",
        "title": "Post from followed user",
        "content": "Content from someone you follow",
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-15T10:30:00Z",
        "comments_count": 2,
        "likes_count": 5,
        "is_liked": false
    }
]
```

### Like Post
**Endpoint:** `POST /api/posts/{id}/like/`

**Headers:**
```
Authorization: Token your-auth-token
```

**Response:**
```json
{
    "message": "Post liked"
}
```

### Unlike Post
**Endpoint:** `POST /api/posts/{id}/unlike/`

**Headers:**
```
Authorization: Token your-auth-token
```

**Response:**
```json
{
    "message": "Post unliked"
}
```

### Get Notifications
**Endpoint:** `GET /api/notifications/`

**Headers:**
```
Authorization: Token your-auth-token
```

**Response:**
```json
[
    {
        "id": 1,
        "actor": "username",
        "verb": "liked your post",
        "target_type": "post",
        "timestamp": "2024-01-15T10:35:00Z",
        "read": false
    },
    {
        "id": 2,
        "actor": "username2",
        "verb": "started following you",
        "target_type": "user",
        "timestamp": "2024-01-15T10:30:00Z",
        "read": true
    }
]
```

### Mark Notification as Read
**Endpoint:** `POST /api/notifications/{id}/read/`

**Headers:**
```
Authorization: Token your-auth-token
```

**Response:**
```json
{
    "message": "Notification marked as read"
}
```

## 🚀 Production Deployment

The Social Media API is production-ready and can be deployed to various platforms:

### Quick Deployment Options

#### Heroku (Recommended for beginners)
```bash
# Run the automated deployment script
chmod +x deploy_heroku.sh
./deploy_heroku.sh
```

#### Docker
```bash
# Build and run with Docker Compose
docker-compose up -d
docker-compose exec web python manage.py migrate
```

#### DigitalOcean
```bash
# Run the DigitalOcean setup script
chmod +x deploy_digitalocean.sh
./deploy_digitalocean.sh
```

### Production Testing
```bash
# Test your deployed API
python test_production_api.py https://your-app-url.com

# Monitor deployment status
python deployment_status.py https://your-app-url.com
```

### Live Demo
- **API URL**: `https://your-deployed-app.herokuapp.com`
- **Admin Panel**: `https://your-deployed-app.herokuapp.com/admin/`
- **API Documentation**: `https://your-deployed-app.herokuapp.com/`

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md)

## Features

### Posts Features
- **CRUD Operations**: Create, read, update, and delete posts
- **Search**: Search posts by title or content using `?search=keyword`
- **Filtering**: Filter posts by author using `?author=user_id`
- **Pagination**: Automatic pagination with 10 posts per page
- **Permissions**: Only authenticated users can create posts, only authors can edit/delete their posts

### Comments Features
- **CRUD Operations**: Create, read, update, and delete comments
- **Filtering**: Filter comments by post or author using `?post=post_id&author=user_id`
- **Permissions**: Only authenticated users can create comments, only authors can edit/delete their comments
- **Nested Relationships**: Comments are linked to both posts and users

### Follow System Features
- **Follow/Unfollow**: Users can follow and unfollow other users
- **Self-Follow Prevention**: Users cannot follow themselves
- **Many-to-Many Relationships**: Efficient handling of follower/following relationships

### Feed Features
- **Personalized Feed**: Shows posts only from users you follow
- **Chronological Order**: Posts ordered by creation date (newest first)
- **Authentication Required**: Only authenticated users can access their feed

### Likes Features
- **Like/Unlike Posts**: Users can like and unlike posts
- **Duplicate Prevention**: Users cannot like the same post multiple times
- **Like Count**: Posts display total number of likes
- **Like Status**: Posts show if current user has liked them
- **Notifications**: Post authors receive notifications when their posts are liked

### Notifications Features
- **Real-time Notifications**: Users receive notifications for interactions
- **Multiple Notification Types**: Likes, comments, and follows generate notifications
- **Read Status**: Notifications can be marked as read/unread
- **Chronological Order**: Notifications ordered by timestamp (newest first)
- **User-specific**: Users only see their own notifications

### Advanced Query Parameters

#### Posts Endpoints
- `GET /api/posts/?search=keyword` - Search in title and content
- `GET /api/posts/?author=user_id` - Filter by author
- `GET /api/posts/?page=2` - Pagination
- `GET /api/posts/?search=keyword&author=user_id&page=1` - Combined filters

#### Comments Endpoints
- `GET /api/comments/?post=post_id` - Filter by post
- `GET /api/comments/?author=user_id` - Filter by author
- `GET /api/comments/?post=post_id&author=user_id` - Combined filters

## Testing with Postman

### Authentication Flow
1. **Register a new user** - POST to `/api/accounts/register/`
2. **Login with credentials** - POST to `/api/accounts/login/`
3. **Access profile** - GET `/api/accounts/profile/` with token header
4. **Update profile** - PUT `/api/accounts/profile/` with token header

### Posts and Comments Flow
5. **Create a post** - POST to `/api/posts/` with token header
6. **List posts** - GET `/api/posts/` (optional: add search parameters)
7. **Update your post** - PUT to `/api/posts/{id}/` with token header
8. **Add a comment** - POST to `/api/comments/` with token header
9. **List comments for a post** - GET `/api/comments/?post={post_id}`
10. **Update your comment** - PUT to `/api/comments/{id}/` with token header

### Follow System and Feed Flow
11. **Follow a user** - POST to `/api/accounts/follow/{user_id}/` with token header
12. **View your feed** - GET `/api/feed/` with token header
13. **Unfollow a user** - POST to `/api/accounts/unfollow/{user_id}/` with token header

### Likes and Notifications Flow
14. **Like a post** - POST to `/api/posts/{post_id}/like/` with token header
15. **View notifications** - GET `/api/notifications/` with token header
16. **Unlike a post** - POST to `/api/posts/{post_id}/unlike/` with token header
17. **Mark notification as read** - POST to `/api/notifications/{notification_id}/read/` with token header

## Testing

### Automated Testing
Run the comprehensive test scripts:
```bash
# Test posts and comments functionality
python test_posts_api.py

# Test follow system and feed functionality
python test_follow_feed.py

# Test likes and notifications functionality
python test_likes_notifications.py
```

### Postman Collection
Import the `Social_Media_API.postman_collection.json` file into Postman for interactive API testing.

### Manual Testing Steps
1. Start the development server: `python manage.py runserver`
2. Register a new user via POST to `/api/accounts/register/`
3. Use the returned token for authenticated requests
4. Test all CRUD operations for posts and comments
5. Verify permissions (users can only edit their own content)
6. Test search and filtering functionality

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
├── posts/
│   ├── migrations/
│   ├── models.py          # Post, Comment, and Like models
│   ├── serializers.py     # Post, Comment, and Like serializers
│   ├── views.py          # Post and Comment viewsets with like functionality
│   ├── urls.py           # Posts app URL patterns
│   └── admin.py          # Admin configuration
├── notifications/
│   ├── migrations/
│   ├── models.py          # Notification model
│   ├── serializers.py     # Notification serializers
│   ├── views.py          # Notification views
│   ├── urls.py           # Notifications URL patterns
│   └── admin.py          # Admin configuration
├── social_media_api/
│   ├── settings.py       # Project settings
│   └── urls.py          # Main URL configuration
├── test_posts_api.py     # Comprehensive API test script
├── test_follow_feed.py   # Follow and feed test script
├── test_likes_notifications.py  # Likes and notifications test script
├── Social_Media_API.postman_collection.json  # Postman collection
└── manage.py
```

## Implementation Details

### Models
- **Post Model**: Contains author (ForeignKey), title, content, timestamps
- **Comment Model**: Contains post (ForeignKey), author (ForeignKey), content, timestamps
- **Like Model**: Contains user (ForeignKey), post (ForeignKey), timestamps with unique constraint
- **Notification Model**: Contains recipient, actor, verb, target (GenericForeignKey), timestamp, read status
- All models include proper ordering and string representations

### Permissions
- **IsAuthorOrReadOnly**: Custom permission class ensuring only authors can modify their content
- **IsAuthenticatedOrReadOnly**: Allows read access to all, write access to authenticated users only

### Features Implemented
- ✅ Complete CRUD operations for posts and comments
- ✅ Token-based authentication
- ✅ Search functionality for posts (title and content)
- ✅ Filtering by author for both posts and comments
- ✅ Filtering comments by post
- ✅ Pagination (10 items per page)
- ✅ Proper permissions and authorization
- ✅ Follow/unfollow system
- ✅ Personalized feed functionality
- ✅ Like/unlike posts functionality
- ✅ Comprehensive notification system
- ✅ Real-time notifications for likes, comments, and follows
- ✅ Notification read/unread status
- ✅ Admin interface integration
- ✅ Comprehensive test coverage