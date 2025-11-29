from django.urls import path
from .views import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

urlpatterns = [
    # List all books
    path('books/', ListView.as_view(), name='book-list'),
    
    # Retrieve a single book by ID
    path('books/<int:pk>/', DetailView.as_view(), name='book-detail'),
    
    # Create a new book
    path('books/create/', CreateView.as_view(), name='book-create'),
    
    # Update an existing book
    path('books/<int:pk>/update/', UpdateView.as_view(), name='book-update'),
    
    # Delete a book
    path('books/<int:pk>/delete/', DeleteView.as_view(), name='book-delete'),
]