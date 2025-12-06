# Django Blog CRUD Operations Documentation

## Overview
This document describes the complete CRUD (Create, Read, Update, Delete) functionality implemented for blog posts in the Django blog application.

## Features Implemented

### 1. CRUD Operations
- **Create**: Authenticated users can create new blog posts
- **Read**: All users can view blog posts (list and detail views)
- **Update**: Only post authors can edit their posts
- **Delete**: Only post authors can delete their posts

### 2. Class-Based Views
- `PostListView`: Displays paginated list of all posts
- `PostDetailView`: Shows individual post details
- `PostCreateView`: Form for creating new posts (login required)
- `PostUpdateView`: Form for editing posts (author only)
- `PostDeleteView`: Confirmation page for deleting posts (author only)

### 3. Permissions and Security
- **LoginRequiredMixin**: Ensures only authenticated users can create posts
- **UserPassesTestMixin**: Ensures only post authors can edit/delete their posts
- **CSRF Protection**: All forms include CSRF tokens

## URL Patterns

| URL | View | Purpose | Access |
|-----|------|---------|--------|
| `/` | PostListView | Home page with post list | Public |
| `/posts/` | PostListView | Blog posts list | Public |
| `/posts/<int:pk>/` | PostDetailView | Individual post | Public |
| `/posts/new/` | PostCreateView | Create new post | Authenticated |
| `/posts/<int:pk>/edit/` | PostUpdateView | Edit post | Author only |
| `/posts/<int:pk>/delete/` | PostDeleteView | Delete post | Author only |

## Templates

### 1. post_list.html
- Displays paginated list of blog posts
- Shows post title, author, date, and content preview
- Includes "New Post" button for authenticated users
- Shows Edit/Delete buttons for post authors

### 2. post_detail.html
- Shows complete post content
- Displays post metadata (author, date)
- Includes Edit/Delete buttons for post authors
- "Back to Posts" navigation link

### 3. post_form.html
- Unified template for create and update operations
- Dynamic title and button text based on operation
- CSRF protection included
- Cancel button returns to post list

### 4. post_confirm_delete.html
- Confirmation page for post deletion
- Warning message about permanent action
- Cancel option returns to post detail

## Forms

### PostForm (ModelForm)
- Fields: title, content
- Author automatically set from logged-in user
- Built-in validation from Django

## Security Features

### Authentication Requirements
```python
# Only authenticated users can create posts
class PostCreateView(LoginRequiredMixin, CreateView):
    # ...

# Only post authors can edit/delete
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
```

### CSRF Protection
All forms include `{% csrf_token %}` to prevent cross-site request forgery attacks.

## Testing Guidelines

### 1. Create Post Testing
1. Login as authenticated user
2. Navigate to `/posts/new/`
3. Fill in title and content
4. Submit form
5. Verify redirect to post detail page

### 2. Edit Post Testing
1. Login as post author
2. Navigate to post detail page
3. Click "Edit" button
4. Modify content
5. Submit form
6. Verify changes are saved

### 3. Delete Post Testing
1. Login as post author
2. Navigate to post detail page
3. Click "Delete" button
4. Confirm deletion
5. Verify post is removed from list

### 4. Permission Testing
1. Try to edit another user's post
2. Verify access is denied (403 error)
3. Try to access create form without login
4. Verify redirect to login page

## Navigation Flow

```
Home (Post List) → Post Detail → Edit/Delete (Author only)
     ↓
New Post (Authenticated) → Post Detail
```

## Model Enhancements

### get_absolute_url Method
```python
def get_absolute_url(self):
    return reverse('post-detail', kwargs={'pk': self.pk})
```
Enables automatic URL generation after form submissions.

## Pagination
- Post list view includes pagination (5 posts per page)
- Navigation controls for previous/next pages
- Page number display

## Styling
- Responsive design using existing CSS
- Button styling for actions
- Alert styling for delete confirmation
- Consistent layout with base template

## Usage Instructions

### For Regular Users
1. Visit the blog to read posts
2. Register/login to create posts
3. Use navigation to browse posts

### For Authors
1. Login to your account
2. Click "New Post" to create content
3. Use Edit/Delete buttons on your posts
4. Manage your content from post detail pages

## Error Handling
- 403 Forbidden for unauthorized edit/delete attempts
- Form validation errors displayed to users
- Proper redirects after successful operations
- Cancel options on all forms