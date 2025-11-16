from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseBadRequest
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Book
from .forms import BookForm, ExampleForm
import logging

# Configure logging for security events
logger = logging.getLogger(__name__)

@permission_required('bookshelf.can_view', raise_exception=True)
@require_http_methods(["GET"])
def book_list(request):
    """
    Secure book listing view with search functionality
    Uses Django ORM to prevent SQL injection
    """
    books = Book.objects.all()
    
    # Secure search functionality using Django ORM
    search_query = request.GET.get('search', '').strip()
    if search_query:
        # Log search attempts for security monitoring
        logger.info(f"Search performed by user {request.user.username}: {search_query}")
        
        # Use Django ORM Q objects for safe querying - prevents SQL injection
        books = books.filter(
            Q(title__icontains=search_query) | 
            Q(author__icontains=search_query)
        )
    
    # Implement pagination to prevent DoS attacks
    paginator = Paginator(books, 10)  # Show 10 books per page
    page_number = request.GET.get('page', 1)
    
    try:
        page_number = int(page_number)
    except (ValueError, TypeError):
        page_number = 1
    
    books = paginator.get_page(page_number)
    
    return render(request, 'bookshelf/book_list.html', {
        'books': books,
        'search_query': search_query
    })

@permission_required('bookshelf.can_create', raise_exception=True)
@csrf_protect
@require_http_methods(["GET", "POST"])
def book_create(request):
    """
    Secure book creation view with CSRF protection and input validation
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            try:
                book = form.save()
                messages.success(request, f'Book "{book.title}" created successfully.')
                logger.info(f"Book created by user {request.user.username}: {book.title}")
                return redirect('book_list')
            except Exception as e:
                logger.error(f"Error creating book by user {request.user.username}: {str(e)}")
                messages.error(request, 'An error occurred while creating the book.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BookForm()
    
    return render(request, 'bookshelf/book_form.html', {
        'form': form, 
        'action': 'Create'
    })

@permission_required('bookshelf.can_edit', raise_exception=True)
@csrf_protect
@require_http_methods(["GET", "POST"])
def book_edit(request, pk):
    """
    Secure book editing view with proper validation
    """
    # Validate pk parameter to prevent injection
    try:
        pk = int(pk)
    except (ValueError, TypeError):
        return HttpResponseBadRequest("Invalid book ID")
    
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            try:
                updated_book = form.save()
                messages.success(request, f'Book "{updated_book.title}" updated successfully.')
                logger.info(f"Book updated by user {request.user.username}: {updated_book.title}")
                return redirect('book_list')
            except Exception as e:
                logger.error(f"Error updating book by user {request.user.username}: {str(e)}")
                messages.error(request, 'An error occurred while updating the book.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BookForm(instance=book)
    
    return render(request, 'bookshelf/book_form.html', {
        'form': form, 
        'action': 'Edit',
        'book': book
    })

@permission_required('bookshelf.can_delete', raise_exception=True)
@csrf_protect
@require_http_methods(["GET", "POST"])
def book_delete(request, pk):
    """
    Secure book deletion view with confirmation
    """
    # Validate pk parameter
    try:
        pk = int(pk)
    except (ValueError, TypeError):
        return HttpResponseBadRequest("Invalid book ID")
    
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        try:
            book_title = book.title
            book.delete()
            messages.success(request, f'Book "{book_title}" deleted successfully.')
            logger.info(f"Book deleted by user {request.user.username}: {book_title}")
            return redirect('book_list')
        except Exception as e:
            logger.error(f"Error deleting book by user {request.user.username}: {str(e)}")
            messages.error(request, 'An error occurred while deleting the book.')
    
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})

@csrf_protect
def form_example(request):
    """
    Example view demonstrating secure form handling
    """
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Process form data securely
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # Log form submission
            logger.info(f"Form submitted by {email}")
            
            messages.success(request, 'Form submitted successfully!')
            return redirect('form_example')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ExampleForm()
    
    return render(request, 'bookshelf/form_example.html', {'form': form})
