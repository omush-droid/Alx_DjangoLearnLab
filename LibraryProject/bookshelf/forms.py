from django import forms
from django.core.exceptions import ValidationError
from .models import Book
import re

class BookForm(forms.ModelForm):
    """
    Secure form for Book model with input validation and sanitization
    """
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 200}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 100}),
            'publication_year': forms.NumberInput(attrs={'class': 'form-control', 'min': 1000, 'max': 2100}),
        }

    def clean_title(self):
        """Validate and sanitize book title"""
        title = self.cleaned_data.get('title')
        if not title:
            raise ValidationError("Title is required.")
        
        # Remove potentially harmful characters
        title = re.sub(r'[<>"\']', '', title)
        
        if len(title.strip()) < 2:
            raise ValidationError("Title must be at least 2 characters long.")
        
        return title.strip()

    def clean_author(self):
        """Validate and sanitize author name"""
        author = self.cleaned_data.get('author')
        if not author:
            raise ValidationError("Author is required.")
        
        # Remove potentially harmful characters
        author = re.sub(r'[<>"\']', '', author)
        
        # Check for valid author name pattern
        if not re.match(r'^[a-zA-Z\s\.\-]+$', author):
            raise ValidationError("Author name contains invalid characters.")
        
        return author.strip()

    def clean_publication_year(self):
        """Validate publication year"""
        year = self.cleaned_data.get('publication_year')
        if not year:
            raise ValidationError("Publication year is required.")
        
        if year < 1000 or year > 2100:
            raise ValidationError("Publication year must be between 1000 and 2100.")
        
        return year

class ExampleForm(forms.Form):
    """
    Example form demonstrating secure form practices
    """
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    message = forms.CharField(
        max_length=1000,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
    )

    def clean_name(self):
        """Sanitize name input"""
        name = self.cleaned_data.get('name')
        # Remove HTML tags and potentially harmful characters
        name = re.sub(r'[<>"\']', '', name)
        return name.strip()

    def clean_message(self):
        """Sanitize message input"""
        message = self.cleaned_data.get('message')
        # Remove script tags and other potentially harmful content
        message = re.sub(r'<script.*?</script>', '', message, flags=re.IGNORECASE | re.DOTALL)
        message = re.sub(r'[<>]', '', message)
        return message.strip()